from flask import Blueprint, request, render_template


from ..models import Driver
from ..services import roundDrivers, getDriver

driver = Blueprint('driver', __name__, template_folder='driver_templates')


@driver.route('/driver/create/<int:round>')
def createDriver(round):
    d_list = roundDrivers(round)
    for d in d_list:
        check = Driver.query.filter_by(id=d).first()
        if check:
            print(check)
        d_dict = getDriver(d)
        first_name = d_dict['first_name']
        last_name = d_dict['last_name']
        nation = d_dict['nation']
        new = Driver(d, first_name, last_name, nation)
        new.saveDriver()
    return {
        'status' : 'OK',
        'message' : 'I THINK this worked??? idk, check the db'
    }
        

