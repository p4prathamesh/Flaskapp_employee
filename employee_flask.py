from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_PORT'] = db['mysql_port']

mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def index():
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM employee_details")
	employeeDetails = cur.fetchall()
	search_result1=[]
	if request.method == 'POST':
		employee = request.form
		search = employee['search']
		search_result = cur.execute("SELECT * FROM employee_details WHERE name=%s or designation=%s or phone=%s",(search,search,search))
		search_result1 = cur.fetchall()
	return render_template('index.html', employeeDetails=employeeDetails, search_result=search_result1)

@app.route('/add_employee', methods=['GET','POST'])
def add_employee():
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		employeeForm = request.form
		name = employeeForm['name']
		designation = employeeForm['designation']
		address = employeeForm['address']
		phone  = employeeForm['phone']
		cur.execute("INSERT INTO employee_details values(%s,%s,%s,%s)",(name,designation,address,phone))
		mysql.connection.commit()
		cur.close()
		return render_template('success.html')
		
	return render_template('form.html')

@app.route('/delete_employee', methods=['GET','POST'])
def delete_employee():
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM employee_details")
	employeeDetails = cur.fetchall()	
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		employeeForm = request.form
		name = employeeForm['name']
		cur.execute("DELETE FROM employee_details WHERE name=%s",(name,))
		mysql.connection.commit()
		cur.close()
		return render_template('delete.html')	
	return render_template('delete_form.html',employeeDetails=employeeDetails)

if __name__ == '__main__':
    app.run(debug=True)