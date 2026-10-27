import tempfile,unittest
from pathlib import Path
import app
class Tests(unittest.TestCase):
 def test_stock_report(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'test.sqlite3';app.add('Pen','PEN-1',5,2,p);self.assertEqual(app.report(p)['units_in_stock'],5)
if __name__=='__main__':unittest.main()
