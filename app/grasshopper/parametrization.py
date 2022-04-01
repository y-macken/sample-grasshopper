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
from viktor.parametrization import HiddenField
from viktor.parametrization import NumberField
from viktor.parametrization import Parametrization
from viktor.parametrization import Step

class GrasshopperParametrization(Parametrization):
    """Defines the input fields in left-side of the web UI in the Grasshopper entity (Editor)."""
    input = Step("visualization stadium", views='visualize')
    input.pitch_width = NumberField("Pitch width", suffix="m", default=70)
    input.Offset = NumberField("Offset from pitch", suffix="m", default=4)
    input.Shape = NumberField("Shape", suffix="m", default=16)
    input.Depth = NumberField("Depth factor", default=1.5)
    input.Asymmetry_length = NumberField("Asymmetry along length", default=20)
    input.Asymmetry_width = NumberField("Asymmetry along width", default=20)
    input.Height = NumberField("Height", suffix="m", default=40)
