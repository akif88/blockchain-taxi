from builtins import print

from flask import Flask, render_template, redirect, url_for, request
import web3_taxi as taxi

app = Flask(__name__)


# initial page
@app.route('/')
@app.route('/<name>')
def index(name=None):
    accounts = taxi.ether_account()

    if name is not None: # get block value that sended by join function
        block = request.args['block']
        return render_template('index.html', name=name, account=accounts, manager=accounts[0], block=block)

    return render_template('index.html', account=accounts, manager=accounts[0])


# get solidity values that sended by web3_taxi
@app.route('/', methods=["POST"])
@app.route('/<name>', methods=["POST"])
def join(name=None):
    if request.method == 'POST':
        btn_value = request.form['join']

        if btn_value == 'join':
            account_address = request.form['account_list']
            block = taxi.taxi_join(account_address)

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'carDealer':
            dealer_address = request.form['account_list']
            block = taxi.set_car_dealer(dealer_address)

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'propose':
            dealer_address = request.form['account_list']
            car_id = request.form['carId']
            price = request.form['price']
            valid_time = request.form['validTime']
            block = taxi.car_propose_to_business(dealer_address, car_id, price, valid_time)

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'approveCar':
            account_address = request.form['account_list']
            block = taxi.approve_purchase_car(account_address)

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'purchaseCar':
            block = taxi.purchase_car()

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'repurchaseCar':
            dealer_address = request.form['account_list']
            car_id = request.form['recarId']
            price = request.form['reprice']
            valid_time = request.form['revalidTime']
            block = taxi.repurchase_car_propose(dealer_address, car_id, price, valid_time)

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'sellProposal':
            account_address = request.form['account_list']
            block = taxi.approve_sell_proposal(account_address)

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'repurchase':
            dealer_address = request.form['account_list']
            price = request.form['repurchase']
            block = taxi.repurchase_car(dealer_address, price)

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'proposeDriver':
            driver_address = request.form['account_list']
            salary = request.form['salary']
            block = taxi.propose_driver(driver_address, salary)

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'approveDriver':
            account_address = request.form['account_list']
            block = taxi.approve_driver(account_address)

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'setDriver':
            block = taxi.set_driver()

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'fireDriver':
            block = taxi.fire_driver()

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'charge':
            account_address = request.form['account_list']
            charge = request.form['charge']
            block = taxi.get_charge(account_address, charge)

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'release':
            block = taxi.release_salary()

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'money':
            driver_address = request.form['account_list']
            money = request.form['money']
            block = taxi.get_salary(driver_address, money)

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'expenses':
            block = taxi.car_expenses()

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'dividend':
            block = taxi.pay_dividend()

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'getDividend':
            account_address = request.form['account_list']
            block = taxi.get_dividend(account_address)

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'getuser':
            block = taxi.get_participant()
            add = ', '.join(block)  # to get query correctly. get just first element if redirect array
            block = add

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'getdealer':
            block = taxi.get_car_dealer()

            return redirect(url_for('index', name="join", block=block))

        if btn_value == 'getdriver':
            block = taxi.get_driver()

            return redirect(url_for('index', name="join", block=block))

    return render_template('index.html', name=name)


if '__name__' == '__main__':
    app.run()
