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
        # TODO make param string
        param_string = f""

        path_to_rhino_file = Path(__file__).parent / 'data' / ''
        path_to_gh_file = Path(__file__).parent / 'data' / 'sample_app_gh.gh'
        path_to_rhino_programm = 'C:\\Program Files\\Rhino 7\\System\\Rhino.exe'

        executable_string = f'SET rhinoFilePath="{path_to_rhino_file}" SET ghFilePath="{path_to_gh_file}"\n ' \
                            f'"{path_to_rhino_programm}" /nosplash /runscript="-open %rhinoFilePath% ' \
                            f'-GrasshopperPlayer {path_to_gh_file} {param_string} _save _enter exit _enter'

        # Generate the input file(s)
        files = [
            ('run_grasshopper.bat', BytesIO(bytes(executable_string,  'utf8')))
        ]

        # Run the analysis and obtain the output file
        generic_analysis = GenericAnalysis(files=files, executable_key="run_grasshopper",
                                           output_filenames=["out.txt"])
        generic_analysis.execute(timeout=60)
        output_file = generic_analysis.get_output_file("out.txt")

        # TODO Parse output data from output string
        # construct data group
        data_group = DataGroup()

        return DataResult(data_group)
