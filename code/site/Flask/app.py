from flask import Flask, render_template
import psycopg2

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/Data')
def Data():
	con = psycopg2.connect("dbname='Project' user='osc' password='osc'")

	cur = con.cursor()
	cur.execute("SELECT tables.table_catalog, tables.table_name, tables.table_type FROM  INFORMATION_SCHEMA.tables WHERE table_schema='public' AND table_type = 'BASE TABLE' ORDER BY tables.table_name;")
	oTables = cur.fetchall()
	cur.close

	cur = con.cursor()
	cur.execute("SELECT * From content")
	cont = cur.fetchall()
	cur.close

	cur = con.cursor()
	cur.execute("SELECT * From article")
	arts = cur.fetchall()
	cur.close

	cur = con.cursor()
	cur.execute("SELECT * From mm")
	mults = cur.fetchall()
	cur.close

	return render_template('data.html', oTables=oTables, cont=cont, arts=arts, mults=mults)
	
@app.route('/Data/County')
def CountyMap():
	return render_template('map.html')

@app.route('/Data/County/<county>')
def CountData(county):
	con = psycopg2.connect("dbname='Project' user='osc' password='osc'")
	cur = con.cursor()
	cur.execute("""SELECT * FROM content WHERE location = (%s); """, (county,))
	cont = cur.fetchall()
	cur.close

	return render_template('cData.html', cont=cont)

if __name__ == '__main__':
	app.run()