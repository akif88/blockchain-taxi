pragma solidity ^0.5.0;

contract TaxiChain {
    
    //---------------
    
    address[] participant; // participant addresslerini atamak için 
    mapping (address => uint256) participantBalance; // participant addresslerine göre paralarını eklemek veya çıkarmak için
    int public totalParticipants; // hoca en fazla 9 tane participant olsun demiş onu tutmak için 
    
    //---------------
    
    address manager; // bu contract ilk kez çağırıldığında çağaran kişinin adresi manager olarak belirlenecek
    uint256 dividendTime; // kar payları 6 ayda bir verilecekmiş 
    uint256 dividend; // calculated every 6 months
    address[] releaseList; // verilen kar payları birden fazla verilmesin diye
    
    //---------------
    struct Driver{  // sürücünün föye göre belirlenen özellikleri
        address driverAddress; 
        uint256 salary; // maaş miktarı
        uint256 releaseSalaryTime; // her ay bir kere verilecek
        int approvalState; // oylama için bu sürücü kaç  participant tarafından onaylandı 
    }
    
    Driver driver; // struct değişkeni ile özellikleri atanacak
    mapping (address => uint256) driverBalances; // sürücü adresi ile para verilip alınacabilecek
    Driver proposedDriver; // manager tarafından önerilen sürücü
    mapping(address => address) approvedDriver; // önerilen sürücünün adresi ve kabul eden participant adresi, kontrol için
    //---------------
    
    address addressCarDealer;
    mapping (address => uint256) carDealer; // para alma verme
    //---------------
    
    uint256 contractBalances; // total money in contract
    mapping (address => uint256) customerBalances; // taksiye binen müşteriden para almak için 
    //---------------
    
    uint256 timeFixedExpenses; // every 6 months
    uint256 carExpensesPrice; // her 6 ayda bir ödenecek miktar
    //---------------
    
    uint256 participantFee = 100 ether; // fix 100 ether
    //---------------
    
    bytes32 CarID; // owned car id
    //---------------
    
    struct ProposedCar{ // car dealer tarafından önerilen araba ve özellikleri
        bytes32 CarID;
        uint256 price;
        uint256 validTime; // önerilen arabanın geçerlilik süresi
        int approvalState; // participantlar tarafından onay sayısı
    }
    
    //---------------
    
    ProposedCar proposedCar;
    mapping(address => bytes32) approveCar; // participant adresleri ve car id, kimler onaylamış görmek ve kontrol etmek için birden fazla vermesin diye
    
    ProposedCar proposedRepurchaseCar; //for owned car, owned CarID - alınan arabanın tekrar car dealer'a satışı için önerilen özellikler tutuluyor
    //---------------

    // display participant join if function execute successfully
    event JoinAccount(address participantAddress, uint256 amount);

    event CarDealerAddress(address carDealerAddress);

    event CarPropose(bytes32 carID, uint256 price, uint256 validTime);

    event ParticipantApprove(address participantAddress);

    event PurchaseCar(bytes32 carID, uint256 price);

    event RePurchaseCar(bytes32 carID, uint256 price, uint256 validTime);

    event SellProposal(address participantAddress);

    event Repurchase(address carDealerAddress, uint256 price);

    event ProposeDriver(address driverAddress, uint256 salary);

    event ApproveDriver(address participantAddress);

    event SetDriver(address driverAddress, uint256 salary);

    event FireDriver(address driverAddress);

    event Charge(address participantAddress, uint256 charge);

    event Release(address driverAddress, uint256 salary, uint256 releaseSalaryTime);

    event GetMoney(address driverAddress, uint256 sendMoney);

    event Expenses(address managerAddress, uint256 carExpensesPrice);

    event Dividend(address managerAddress, uint256 dividend);

    event GetDividend(address participantAddress, uint256 dividend);

    constructor() public { // java daki sınıf yapısındaki başlangıç fonksiyonu benzeri
        manager = msg.sender; // constructor'u çağıran kişinin adresi manager adresine eşleniyor 
        totalParticipants = 0; // mevcut participant sayısı  
        contractBalances = 0 ether; // mevcut contract parası
        carExpensesPrice = 10 ether; // her 6 ayda bir 10 ether fix vergi ve bakım parası ödenecek car dealer'a 
        dividendTime = now; // kar payı zamanını belirlemek için 6 ayda bir 
    }
    
    function join() payable public { // participant bu fonksiyonu çağırarak katılabilecek
        require(msg.sender.balance >= 10 ether); // en az 100 ether'i olmak zorunda
        require(msg.value == 10 ether); // 100 ether karşılığında katılabilecek
        require(totalParticipants < 9); // en fazla 9 kişi katılabilir
        
        participant.push(msg.sender); // fonksiyonu çağıran participant adresi yukardaki koşullar sağlanırsa eklenecek 
        participantBalance[msg.sender] = msg.sender.balance; // participant'ın mevcut parası
        contractBalances += msg.value; // mevcut paradan 100 ether contract parasına ekleniyor
        participantBalance[msg.sender] -= msg.value; // mevcut parasından 100 ether azaltıldı
        totalParticipants += 1; // bir katılımcı arttır

        // emit event if participant join in taxi blockchain
        emit JoinAccount(msg.sender, msg.sender.balance);
    }
    
    function setCarDealer(address payable _addressCarDealer) public {  // manager istediği bir car dealer adresi ile fonksiyonu çağırabilir
        require(msg.sender == manager); // fonksiyonu çağıran manager mı kontrol et
        addressCarDealer = _addressCarDealer; // koşul sağlandıysa adresi ata

        emit CarDealerAddress(addressCarDealer);
    }
    
    function carProposeToBusiness(bytes32 carID, uint256 price, uint256 validTime) public { // car dealer'ın önerdiği araba
        require(msg.sender == addressCarDealer); // car dealer çağırabilecek sadece
       
        proposedCar.CarID = carID; // koşullar sağlanırsa önerilen arabanın ID'si
        proposedCar.price = price * 10 ** uint256(18); // convert wei to ether with 10^18
        proposedCar.validTime = now + validTime; // geçerlilik süresi
        proposedCar.approvalState = 0; // participant tarafından verilecek oy başlatma

        emit CarPropose(proposedCar.CarID, proposedCar.price, proposedCar.validTime);
    }
    
    
    // participant'ın çağırması gereken fonksiyonlarda adresi göndererek kontrol yapmak için
    function isParticipant(address userAddress) internal view returns(bool) {
        for(uint i= 0; i < participant.length; i++){
            if(participant[i] == userAddress){
                return true; // participant ise true döndür
            }
        }
        return false;
    }
    
    //--------------------approve start----------------------------
    function approvePurchaseCar() public{ // car dealer tarafından önerilen arabanın participant tarafından oylanması
        require(isParticipant(msg.sender)); // fonksiyonu çağıran participant mı
        require(carIDApproveControl(proposedCar.CarID, msg.sender)); // daha önce oy kullandı mı
        require(proposedCar.validTime <= now); // süresi devam ediyor mu
        proposedCar.approvalState += 1; // koşullar sağlandıysa bir arttır

        emit ParticipantApprove(msg.sender);
    }
    
    // participant'ın birden fazla onaylama yapmasını engellemek için
    function carIDApproveControl(bytes32 carID, address addressParticipant) internal returns(bool) {
        if(approveCar[addressParticipant] != carID) { // glabal değişkeni ile participant address carID eşleme  
            approveCar[addressParticipant] = carID;
            return true;
        }
        
        return false;
    }
    // -------------------approve end-----------------------------
    
    function purchaseCar() payable public { // gerekli koşullar sağlanırsa manager tarafından çağırılır ve araba satın alınır
        require(msg.sender == manager); // fonksiyonu çağıran manager mı
        require(proposedCar.validTime <= now); // önerilen arabanın süresi dolmuş mu
        require(proposedCar.approvalState >= (totalParticipants/2)+1); // participantların yarısından bir fazlası onaylamak zorunda 
        require(contractBalances >= proposedCar.price); // contracttaki para arabayı almaya yetiyor mu
        
        carDealer[addressCarDealer] += proposedCar.price; // parayı car dealer'a ver
        contractBalances -= proposedCar.price; // contracttaki parayı azalt
        CarID = proposedCar.CarID;  // assign proposed car id to purchased car id 
        timeFixedExpenses = now; // vergiler ve bakım için 6 aylık süreyi başlat

        emit PurchaseCar(CarID, proposedCar.price);
    }
    
    function repurchaseCarPropose(uint256 price, uint256 validTime) public { // arabayı satmak için
        require(msg.sender == addressCarDealer); // fonksiyonu car dealer çağırır
        
        // arabayı almak için teklifleri 
        proposedRepurchaseCar.CarID = CarID; // mevcut arabanın ID'si
        proposedRepurchaseCar.price = price; // teklif edilen para
        proposedRepurchaseCar.validTime = now + validTime; // geçerlilik süresi
        proposedRepurchaseCar.approvalState = 0; // onay başlat

        emit RePurchaseCar(proposedRepurchaseCar.CarID, proposedRepurchaseCar.price, proposedRepurchaseCar.validTime);
    }
    
    function approveSellProposal() public { // onaylama fonkiyonu repurchaseCarPropose için
        require(isParticipant(msg.sender)); // participant olmalı
        require(carIDApproveControl(proposedRepurchaseCar.CarID, msg.sender)); // tek onaylama yapmak için
        require(proposedRepurchaseCar.validTime <= now); // süre kontrol
        proposedRepurchaseCar.approvalState += 1; // koşullar sağlandıysa bir arttır

        emit SellProposal(msg.sender);
    }

    function repurchaseCar() payable public { // onaylanırsa
        require(msg.sender == addressCarDealer);
        require(proposedRepurchaseCar.validTime <= now);
        require(proposedRepurchaseCar.approvalState >= (totalParticipants/2)+1);
        
        contractBalances += msg.value; // arabayı sat

        emit Repurchase(msg.sender, msg.value);
    }
    
    function proposeDriver(address payable addressDriver, uint256 salary) public { // manager tarafından önerilen sürücü  
        require(msg.sender == manager); 
        
        //önerilen sürücü için
        proposedDriver.driverAddress = addressDriver; 
        proposedDriver.salary = salary; // maaş
        proposedDriver.approvalState = 0; // onay

        emit ProposeDriver(proposedDriver.driverAddress, proposedDriver.salary);
    }
    
    //--------------------approve driver start----------------------------
    function approveDriver() public { // sürücü onaylama  
        require(isParticipant(msg.sender));
        require(driverApproveControl(proposedDriver.driverAddress, msg.sender));
        
        proposedDriver.approvalState +=1;

        emit ApproveDriver(msg.sender);
    }
    
    // participant'ın sadece bir kez onaylama yapabilmesi için
    function driverApproveControl(address driverAddress, address addressParticipant) internal returns(bool) {
        if(approvedDriver[addressParticipant] != driverAddress) {
            approvedDriver[addressParticipant] = driverAddress;
            return true;
        }
        
        return false;
    }
    //-------------------approve driver end-----------------------------
    
    function setDriver() public { // sürücü onaylanırsa
        require(msg.sender == manager);
        require(proposedDriver.approvalState >= (totalParticipants/2)+1);
        
        driver.driverAddress = proposedDriver.driverAddress;
        driver.salary = proposedDriver.salary;
        driver.releaseSalaryTime = now; // ayda bir maaş veilecek
        driverBalances[driver.driverAddress] = 0; // sürücü parası

        emit SetDriver(driver.driverAddress, driver.salary);
    }
    
    function fireDriver() public { // sürücü kov
        require(msg.sender == manager);
        require(contractBalances >= driver.salary);
        
        // sürücü kovulursa bir aylık maaş ödemsi yapılır.
        driverBalances[driver.driverAddress] += driver.salary;
        contractBalances -= driver.salary;

        emit FireDriver(driver.driverAddress);

        delete driver;
    }
    
    function getCharge() payable public { // müşteri taksi ücreti ödemesi
        require(customerBalances[msg.sender] >= msg.value);
        
        customerBalances[msg.sender] -= msg.value;
        contractBalances += msg.value;

        emit Charge(msg.sender, msg.value);
    }
    
    function releaseSalary() public { //sürücüye  her ay maaş ver
        require(msg.sender == manager);
        require((driver.releaseSalaryTime + now) >= 4 weeks); // 1ay içinde birden fazla verme
        require(contractBalances >= driver.salary);
        
        driverBalances[driver.driverAddress] += driver.salary;
        contractBalances -= driver.salary;
        driver.releaseSalaryTime = now;

        emit Release(driver.driverAddress, driver.salary, driver.releaseSalaryTime);
    }
    
    function getSalary(address payable accountDriver, uint256 sendMoney) public { //sürücünün kendi adresine para aktarması için
        require(msg.sender == driver.driverAddress);
        require(driverBalances[msg.sender] >= sendMoney);
        
        customerBalances[accountDriver] += sendMoney;
        contractBalances -= sendMoney;

        emit GetMoney(driver.driverAddress, sendMoney);
    }
    
    function carExpenses() public { // 6 aylık vergi ve bakım parası
        require(msg.sender == manager);
        require(timeFixedExpenses + now >= 4*6 weeks);
        require(contractBalances >= carExpensesPrice);
        
        carDealer[addressCarDealer] += carExpensesPrice;
        contractBalances -= carExpensesPrice;

        emit Expenses(msg.sender, carExpensesPrice);
    }
    
    function payDividend() public { // ayda bir participant'a kar ödemesi hesabı
        require(msg.sender == manager);
        require(dividendTime + now >= 4*6 weeks);
        require(contractBalances > 0);
        
        dividend = contractBalances / uint256(totalParticipants); 
        delete releaseList; // reset releaseList

        emit Dividend(msg.sender, dividend);
    }
    
    // kardan payını birden fazla almasını engellemek için
    function isReleaseList(address userAddress) internal view returns(bool) {
        for(uint i= 0; i < releaseList.length; i++){
            if(releaseList[i] == userAddress){
                return false;
            }
        }
        return true;
    }
    
    function getDividend() public { // kar payını almak için
        require(isParticipant(msg.sender));
        require(isReleaseList(msg.sender));
        
        participantBalance[msg.sender] += dividend;
        releaseList.push(msg.sender);

        emit GetDividend(msg.sender, dividend);
    }

    function getParticipant() public returns(address[] memory) {
        return participant;
    }

    function getCarDealer() public returns(address) {
        return addressCarDealer;
    }

    function getDriver() public returns(address) {
        return driver.driverAddress;
    }
}


