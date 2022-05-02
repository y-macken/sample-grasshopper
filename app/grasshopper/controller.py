"""Copyright (c) 2022 VIKTOR B.V.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

VIKTOR B.V. PROVIDES THIS SOFTWARE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from io import BytesIO
from io import TextIOWrapper
from pathlib import Path

from trimesh import load
from trimesh.exchange.gltf import export_glb
from trimesh.resolvers import FilePathResolver
from viktor import File
from viktor import UserException
from viktor.core import Storage
from viktor.core import ViktorController
from viktor.core import progress_message
from viktor.external.generic import GenericAnalysis
from viktor.result import DownloadResult
from viktor.views import DataGroup
from viktor.views import DataItem
from viktor.views import GeometryAndDataResult
from viktor.views import GeometryAndDataView

from .parametrization import GrasshopperParametrization


class GrasshopperController(ViktorController):
    """Controller class which acts as interface for the Grasshopper entity type."""
    label = "Grasshopper"
    parametrization = GrasshopperParametrization
    viktor_convert_entity_field = True

    @GeometryAndDataView('3D model', duration_guess=10, up_axis='Y')
    def visualize(self, params, **kwargs):
        """Visualizes the 3d model of the grasshopper design and displays the data returned from it."""
        # Create all files needed to send to the worker. This is the Rhino file, the Grasshopper file,
        # and the input parameters as a txt file
        with open(Path(__file__).parent / 'data' / 'sample_app.3dm', 'rb') as rhino_file:
            rhino_file_buffer = BytesIO(rhino_file.read())
        with open(Path(__file__).parent / 'data' / 'sample_app_gh.gh', 'rb') as grasshopper_file:
            grasshopper_file_buffer = BytesIO(grasshopper_file.read())
        input_str = f'{params.grasshopper.pitch_width}, {params.grasshopper.Offset}, {params.grasshopper.Shape}, ' \
                    f'{params.grasshopper.Depth}, {params.grasshopper.Asymmetry_length}, ' \
                    f'{params.grasshopper.Asymmetry_width}, {params.grasshopper.Height}'
        files = [
            ('input.txt', BytesIO(bytes(input_str, 'utf8'))),
            ('sample_app.3dm', rhino_file_buffer),
            ('sample_app_gh.gh', grasshopper_file_buffer)
        ]

        progress_message(message='1/3 - Opening Rhino and grasshopper to export the obj file (±3 min)')

        # Run the analysis on grasshopper
        generic_analysis = GenericAnalysis(files=files, executable_key="run_grasshopper",
                                           output_filenames=["output.txt", "output.obj", "output.mtl"])
        generic_analysis.execute(timeout=300)

        # Retrieve all files from the analysis
        grass_hopper_data_bytes = generic_analysis.get_output_file("output.txt")
        object_file = generic_analysis.get_output_file("output.obj")
        material_file = generic_analysis.get_output_file("output.mtl")

        # Parse output.txt to an array (split by lines)
        wrapper = TextIOWrapper(grass_hopper_data_bytes, encoding='utf-8')
        grass_hopper_data = wrapper.read().splitlines()

        amount_of_seats = grass_hopper_data[0]
        field_length = float(grass_hopper_data[1]) * 2
        field_width = float(grass_hopper_data[2]) * 2

        progress_message(message='2/3 - Convert obj bytes to glb file (±2 min)')

        # convert obj bytes to glb file
        resolver = FilePathResolver(str(Path(__file__).parent))
        resolver.write("output.mtl", TextIOWrapper(material_file).read())
        trimesh_scene = load(object_file, resolver=resolver, file_type="obj")
        geometry = File()  # create a writable file
        with geometry.open_binary() as writable_buffer:
            writable_buffer.write(export_glb(trimesh_scene))

        # Create results for dataview
        seats_amount = DataGroup(DataItem("Number of seats", amount_of_seats),
                                 DataItem("Field width", field_width),
                                 DataItem("Field length", field_length))

        progress_message(message='3/3 - Store gbl file in memory (±1 min)')

        # store glb file in storage
        storage = Storage()
        storage.set('glb_file', data=geometry, scope='workspace')

        return GeometryAndDataResult(geometry, seats_amount)

    def download_glb_output(self, params, **kwargs):
        """"Download glb file"""
        try:
            storage = Storage()
            glb_file = storage.get('glb_file', scope='workspace')
        except FileNotFoundError as err:
            raise UserException("First update your view") from err

        return DownloadResult(glb_file, 'viktor.glb')
