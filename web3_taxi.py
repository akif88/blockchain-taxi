from web3 import Web3, EthereumTesterProvider
from web3 import eth, personal
from solc import compile_source

# Ethereum Test Environment, created 10 account with 100 ether
w3 = Web3(EthereumTesterProvider())

# read smart contract
with open("taxichain5.sol") as f:
    taxi_solc = f.read()

# compile smart contract
compiled_sol = compile_source(taxi_solc)
contract_interface = compiled_sol['<stdin>:TaxiChain']

# to display ethereum accounts
w3_eth = eth.Eth(w3)

# Create taxi contract
Taxi = w3_eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# assign default account as manager
w3_eth.defaultAccount = w3_eth.accounts[0]

# initial smart contract with solidity constructor function
tx_hash = Taxi.constructor().transact()
tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)  # wait mining

# assign variable created by constructor function
# to use all function on smart contract that created specific contract address
taxi_block = w3_eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)

# get all account (created 10 account by EthereumTesterProvider())
def ether_account():
    accounts = w3_eth.accounts
    # print(accounts)
    return accounts

# to join participant
def taxi_join(ether_account):
    tx_hash = taxi_block.functions.join().transact(
        {
            "from": ether_account,
            "value": w3.toWei(10, 'ether'),
            "gas":  3000000

        }
    )
    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_join_control = taxi_block.events.JoinAccount().processReceipt(tx_receipt)

    if not log_join_control:  # check event tuple empty
        log_join_control = ''  # for prevent error (bad request)

    return log_join_control


def set_car_dealer(carDealer_address):
    tx_hash = taxi_block.functions.setCarDealer(carDealer_address).transact(
        {
            "from": w3_eth.defaultAccount,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_car_dealer_address = taxi_block.events.CarDealerAddress().processReceipt(tx_receipt)

    if not log_car_dealer_address:  # check event tuple empty
        log_car_dealer_address = ''  # for prevent error (bad request)

    return log_car_dealer_address

def car_propose_to_business(carDealer_address, carID, price, validTime):
    tx_hash = taxi_block.functions.carProposeToBusiness(str(carID).encode(), int(price), int(validTime)).transact(
        {
            "from": carDealer_address,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_car_propose_to_business = taxi_block.events.CarPropose().processReceipt(tx_receipt)

    if not log_car_propose_to_business:  # check event tuple empty
        log_car_propose_to_business = ''  # for prevent error (bad request)

    return log_car_propose_to_business

def approve_purchase_car(participant_address):
    tx_hash = taxi_block.functions.approvePurchaseCar().transact(
        {
            "from": participant_address,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_approve_purchase_car = taxi_block.events.ParticipantApprove().processReceipt(tx_receipt)

    if not log_approve_purchase_car:  # check event tuple empty
        log_approve_purchase_car = ''  # for prevent error (bad request)

    return log_approve_purchase_car

def purchase_car():
    tx_hash = taxi_block.functions.approvePurchaseCar().transact(
        {
            "from": w3_eth.defaultAccount,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_purchase_car = taxi_block.events.PurchaseCar().processReceipt(tx_receipt)

    if not log_purchase_car:  # check event tuple empty
        log_purchase_car = ''  # for prevent error (bad request)

    return log_purchase_car


def repurchase_car_propose(carDealer_address, price, valid_time):
    tx_hash = taxi_block.functions.repurchaseCarPropose(price, valid_time).transact(
        {
            "from": carDealer_address,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_repurchase_car_propose = taxi_block.events.RePurchaseCar().processReceipt(tx_receipt)

    if not log_repurchase_car_propose:  # check event tuple empty
        log_repurchase_car_propose = ''  # for prevent error (bad request)

    return log_repurchase_car_propose


def approve_sell_proposal(participant_address):
    tx_hash = taxi_block.functions.approveSellProposal().transact(
        {
            "from": participant_address,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_approve_sell_proposal = taxi_block.events.RePurchaseCar().processReceipt(tx_receipt)

    if not log_approve_sell_proposal:  # check event tuple empty
        log_approve_sell_proposal = ''  # for prevent error (bad request)

    return log_approve_sell_proposal


def repurchase_car(carDealer_address, price):
    tx_hash = taxi_block.functions.repurchaseCar().transact(
        {
            "from": carDealer_address,
            "value": int(price),
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_repurchase_car = taxi_block.events.Repurchase().processReceipt(tx_receipt)

    if not log_repurchase_car:  # check event tuple empty
        log_repurchase_car = ''  # for prevent error (bad request)

    return log_repurchase_car


def propose_driver(addressDriver, salary):
    tx_hash = taxi_block.functions.proposeDriver(addressDriver, int(salary)).transact(
        {
            "from": w3_eth.defaultAccount,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_propose_driver = taxi_block.events.ProposeDriver().processReceipt(tx_receipt)

    if not log_propose_driver:  # check event tuple empty
        log_propose_driver = ''  # for prevent error (bad request)

    return log_propose_driver


def approve_driver(participant_address):
    tx_hash = taxi_block.functions.approveDriver().transact(
        {
            "from": participant_address,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_approve_driver = taxi_block.events.ApproveDriver().processReceipt(tx_receipt)

    if not log_approve_driver:  # check event tuple empty
        log_approve_driver = ''  # for prevent error (bad request)

    return log_approve_driver


def set_driver():
    tx_hash = taxi_block.functions.setDriver().transact(
        {
            "from": w3_eth.defaultAccount,
            "gas": 3000000
        }
    )


    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_set_driver = taxi_block.events.SetDriver().processReceipt(tx_receipt)

    if not log_set_driver:  # check event tuple empty
        log_set_driver = ''  # for prevent error (bad request)

    return log_set_driver

def fire_driver():
    tx_hash = taxi_block.functions.fireDriver().transact(
        {
            "from": w3_eth.defaultAccount,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_fire_driver = taxi_block.events.FireDriver().processReceipt(tx_receipt)

    if not log_fire_driver:  # check event tuple empty
        log_fire_driver = ''  # for prevent error (bad request)

    return log_fire_driver


def get_charge(participant_address, charge):
    tx_hash = taxi_block.functions.getCharge().transact(
        {
            "from": participant_address,
            "value": int(charge),
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_get_charge = taxi_block.events.Charge().processReceipt(tx_receipt)

    if not log_get_charge:  # check event tuple empty
        log_get_charge = ''  # for prevent error (bad request)

    return log_get_charge


def release_salary():
    tx_hash = taxi_block.functions.releaseSalary().transact(
        {
            "from": w3_eth.defaultAccount,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_release_salary = taxi_block.events.Release().processReceipt(tx_receipt)

    if not log_release_salary:  # check event tuple empty
        log_release_salary = ''  # for prevent error (bad request)

    return log_release_salary

def get_salary(address_driver, send_money):
    tx_hash = taxi_block.functions.getSalary(address_driver, send_money).transact(
        {
            "from": address_driver,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_get_salary = taxi_block.events.GetMoney().processReceipt(tx_receipt)

    if not log_get_salary:  # check event tuple empty
        log_get_salary = ''  # for prevent error (bad request)

    return log_get_salary


def car_expenses():
    tx_hash = taxi_block.functions.carExpenses().transact(
        {
            "from": w3_eth.defaultAccount,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_car_expenses = taxi_block.events.Expenses().processReceipt(tx_receipt)

    if not log_car_expenses:  # check event tuple empty
        log_car_expenses = ''  # for prevent error (bad request)

    return log_car_expenses


def pay_dividend():
    tx_hash = taxi_block.functions.payDividend().transact(
        {
            "from": w3_eth.defaultAccount,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_pay_dividend = taxi_block.events.Dividend().processReceipt(tx_receipt)

    if not log_pay_dividend:  # check event tuple empty
        log_pay_dividend = ''  # for prevent error (bad request)

    return log_pay_dividend


def get_dividend(participant_address):
    tx_hash = taxi_block.functions.getDividend().transact(
        {
            "from": participant_address,
            "gas": 3000000
        }
    )

    tx_receipt = w3_eth.waitForTransactionReceipt(tx_hash)
    log_get_dividend = taxi_block.events.GetDividend().processReceipt(tx_receipt)

    if not log_get_dividend:  # check event tuple empty
        log_get_dividend = ''  # for prevent error (bad request)

    return log_get_dividend


def get_participant():
    participants = taxi_block.functions.getParticipant().call()

    return participants


def get_car_dealer():
    car_dealer = taxi_block.functions.getCarDealer().call()

    return car_dealer


def get_driver():
    car_driver = taxi_block.functions.getDriver().call()

    return car_driver
