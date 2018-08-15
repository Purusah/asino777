contract_source_code = '''
 pragma solidity ^0.4.7;
contract Roulette777 {
    address owner;
    uint minBet;
    uint maxBet;
    uint balance;
    uint blockDelay;
    uint blockExpiration;
    
    enum BetTypes{number, color, parity, dozen, column, lowhigh}
    struct Gamble {
        address player;
        uint wager;
        bool spinned; //Was the rouleth spinned ?
        bool win;
        BetTypes betType; //Possible bet types
        uint8 input; //stores number, color, dozen or oddeven
        bool refunded;
        uint8 wheelResult;
        uint256 blockBet; //block of bet
        uint256 blockSpinned; //block of spin
    }
    Gamble[] private gambles;
    
    //current gamble index of the player
    mapping (address=>uint) gambleIndex; 
    //records current status of player
    enum Status {waitingForBet, waitingForSpin} mapping (address=>Status) playerStatus;
    
    constructor () {
        owner = msg.sender;
        minBet = 0;
        maxBet = 100;
        blockDelay = 0;
        blockExpiration = 1000;
    }

    // ### MODIFIERS ###
    modifier ownerOnly() {
        require(msg.sender == owner);
        _;
    }
    
    
    // ### SETTINGS ###
    function changeOwner(address addr) public ownerOnly {
        owner = msg.sender;
    }
    
    function getOwner() view public returns (address) {
        return owner;
    }
    
    function whoAmI() public returns (address) {
        return msg.sender;
    }
    
    function getBet(uint index) public returns (address, uint, bool, bool) {
        // require(index < gambles.length);
        // require(index > 0);
        return (gambles[index].player, gambles[index].wager, gambles[index].spinned, gambles[index].win);
        // return gambles.length;
    }
    
    
    
    // ### BANK BALANCE ###
    function getBalance() view public returns (uint) {
        return balance;
    }
    function updateBalance(uint amount) returns (uint){
        require(balance + amount >= balance);
        balance = amount + balance;
        return balance;
    }
    
    function withdrawBalance(uint sum) ownerOnly public returns (uint) {
        // check bets residuals
        require(balance - sum > 0);
        balance = balance - sum;
        return balance;
    }
    
       
    // ### BET TYPES ###
    function betOnNumber(uint8 numberChosen, uint amount) public returns (uint) {
        //check that number chosen is valid and records bet
        require(numberChosen < 37);
        uint index = placeBet(BetTypes.number, numberChosen, amount);
        return index;
    }
    
    
    // ### BET WORKAROUND ###
    
    function placeBet(BetTypes betType, uint8 input, uint amount) private returns (uint) {
        if (playerStatus[msg.sender] == Status.waitingForSpin) {
            SpinTheWheel(msg.sender);
        }
        playerStatus[msg.sender] = Status.waitingForSpin;
        gambleIndex[msg.sender] = gambles.length;
        uint betValue = checkBetValue(amount);
        gambles.push(Gamble(msg.sender, betValue, false, false, betType, input, false, 37, block.number, 0));
        return gambles.length - 1;
        //refund excess bet (at last step vs re-entry)
        //if (betValue < amount) {
        //  return (msg.sender.send(amount-betValue)==false);
        //}
    }
    
    function checkBetValue(uint amount) private returns (uint playerBetValue) {
        require(amount > minBet);
        require(amount * 35 <= balance);
        if (amount > maxBet) {
            playerBetValue = maxBet;
        }
        else {
            playerBetValue = amount;
        }
        return playerBetValue;
    }
    
    function spinWheel(address spinForPlayer) returns (uint) {
        return SpinTheWheel(spinForPlayer);
    }
    
        // !!! Close bet
    function SpinTheWheel(address spinForPlayer) private returns (uint) {
        if (spinForPlayer == 0) {
            spinForPlayer = msg.sender;
        }
        require(playerStatus[spinForPlayer] == Status.waitingForSpin);
        require(gambles[gambleIndex[spinForPlayer]].spinned == false);
        uint256 betBlock = gambles[gambleIndex[spinForPlayer]].blockBet;
        
        require(block.number >= betBlock + blockDelay);
        
        if (block.number > betBlock + blockExpiration) {
            closeBet(msg.sender, 37, false, 0, 0, 0);
            return 57;
        }
        else {
            uint8 wheelNumber;
            bytes32 blockHash= blockhash(betBlock+blockDelay);
            bytes32 zero = 0;
            // require(blockHash != zero);
            // generate the hash for RNG from the blockHash and the player's address
            bytes32 hashResult = keccak256(abi.encodePacked(blockHash));
            // get the final wheel result
            wheelNumber = uint8(uint256(hashResult)%37);
            //check result against bet and pay if win
            return checkBetResult(wheelNumber, spinForPlayer, blockHash, hashResult);
        }
    }
    

    function checkBetResult(uint8 result, address player, bytes32 blockHash, bytes32 hashResult) private returns(uint) {
        BetTypes betType=gambles[gambleIndex[player]].betType;
        //bet on Number
        if (betType==BetTypes.number) return checkBetNumber(result, player, blockHash, hashResult);
    }
    
    
    // function solve Bet once result is determined : sends to winner, adds loss to profit
    function closeBet(address player, uint8 result, bool win, uint8 multiplier, bytes32 blockHash, bytes32 shaPlayer) private returns (uint){
        //Update status and record spinned
        playerStatus[player]=Status.waitingForBet;
        gambles[gambleIndex[player]].wheelResult=result;
        gambles[gambleIndex[player]].spinned=true;
        gambles[gambleIndex[player]].blockSpinned=block.number;
        uint bet_v = gambles[gambleIndex[player]].wager;
        if (win) {
            gambles[gambleIndex[player]].win=true;
            uint win_v = (multiplier-1)*bet_v;
            //send win!
            //safe send vs potential callstack overflowed spins
            //assert(player.send(win_v+bet_v)!=false);
            return win_v+bet_v;
        }
        else return uint(result);
    }
    // ### Check bet ###
    
    function checkBetNumber(uint8 result, address player, bytes32 blockHash, bytes32 shaPlayer) private returns(uint) {
    // checkbeton number(input)
    // bet type : number
    // input : chosen number 
        bool win;
        if (result==gambles[gambleIndex[player]].input) {
            win=true;  
        }
        return closeBet(player, result, win, 36, blockHash, shaPlayer);
    }
    
}
'''