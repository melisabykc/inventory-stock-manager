import argparse,json,sqlite3
from pathlib import Path
DB=Path(__file__).with_name('data.sqlite3')
def connect(path=DB):
 c=sqlite3.connect(str(path));c.row_factory=sqlite3.Row;c.execute('CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY,name TEXT NOT NULL,sku TEXT UNIQUE NOT NULL,quantity INTEGER NOT NULL,unit_price REAL NOT NULL)');return c
def add(name,sku,quantity,unit_price,path=DB):
 quantity=int(quantity);unit_price=float(unit_price)
 if quantity<0 or unit_price<0 or not name.strip() or not sku.strip():raise ValueError('name and SKU required; quantity and price must be nonnegative')
 with connect(path) as c:cur=c.execute('INSERT INTO products(name,sku,quantity,unit_price) VALUES(?,?,?,?)',(name,sku,quantity,unit_price));return cur.lastrowid
def listing(path=DB):
 with connect(path) as c:return [dict(r) for r in c.execute('SELECT * FROM products ORDER BY name')]
def report(path=DB):
 rows=listing(path);return {'product_count':len(rows),'units_in_stock':sum(r['quantity'] for r in rows),'stock_value':round(sum(r['quantity']*r['unit_price'] for r in rows),2)}
def main():
 p=argparse.ArgumentParser(description='Inventory stock manager');s=p.add_subparsers(dest='cmd',required=True);a=s.add_parser('add');a.add_argument('--name',required=True);a.add_argument('--sku',required=True);a.add_argument('--quantity',type=int,required=True);a.add_argument('--unit-price',type=float,required=True);s.add_parser('list');s.add_parser('report');x=p.parse_args()
 if x.cmd=='add':print(json.dumps({'id':add(x.name,x.sku,x.quantity,x.unit_price)}))
 elif x.cmd=='list':print(json.dumps(listing(),indent=2))
 else:print(json.dumps(report(),indent=2))
if __name__=='__main__':main()
