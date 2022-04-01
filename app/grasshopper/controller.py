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
from pathlib import Path

from viktor.core import ViktorController
from viktor.external.generic import GenericAnalysis
from viktor.views import DataGroup
from viktor.views import DataItem
from viktor.views import DataResult
from viktor.views import DataView

from .parametrization import GrasshopperParametrization


class GrasshopperController(ViktorController):
    """Controller class which acts as interface for the Grasshopper entity type."""
    label = "Grasshopper"
    parametrization = GrasshopperParametrization
    viktor_convert_entity_field = True

    @DataView('Data output', duration_guess=10)
    def visualize(self, params, **kwargs):
        exec_string = '"C:\\Program Files\\Rhino 7\\System\\Rhino.exe" /nosplash /runscript=" -open sample_app.3dm ' \
                      '-Grasshopper _Document _Open sample_app_gh.gh _save _enter exit _enter"\nexit'

        with open(Path(__file__).parent / 'data' / 'sample_app.3dm', 'rb') as rhino_file:
            rhino_file_buffer = BytesIO(rhino_file.read())

        with open(Path(__file__).parent / 'data' / 'sample_app_gh.gh', 'rb') as grasshopper_file:
            grasshopper_file_buffer = BytesIO(grasshopper_file.read())

        files = [
            ('input.txt', BytesIO(bytes('70, 4, 16, 1.5, 20, 20, 40', 'utf8'))),
            # ('run_grassHopper.bat', BytesIO(bytes(exec_string, 'utf8'))),
            ('sample_app.3dm', rhino_file_buffer),
            ('sample_app_gh.gh', grasshopper_file_buffer)
        ]

        # Run the analysis and obtain the output file
        generic_analysis = GenericAnalysis(files=files, executable_key="run_grasshopper",
                                           output_filenames=["output.txt"])
        generic_analysis.execute(timeout=60)
        output_file = generic_analysis.get_output_file("output.txt")

        # TODO Parse output data from output string
        # construct data group
        data_group = DataGroup(DataItem('test', True))

        return DataResult(data_group)
