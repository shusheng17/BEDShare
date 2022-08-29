pragma solidity ^0.4.24;
import "./LibLinkedList.sol";
contract DataContract {

    using LibLinkedList for LibLinkedList.LinkedList;
    LibLinkedList.LinkedList public link;
    mapping(uint => LibLinkedList.LinkedList) public edb;
    
    // string类型转化为bytes32类型
    function strTobytes32(string memory source) constant internal returns(bytes32 result){

    	assembly{
    	result := mload(add(source,32))
    	}
    }
    
    // bytes32类型转化为string类型
    function bytes32Tostr(bytes32 x) constant internal returns(string){

        bytes memory bytesString = new bytes(32);
        uint charCount = 0 ;
        for(uint j = 0 ; j<32;j++){
            byte char = byte(bytes32(uint(x) *2 **(8*j)));
            if(char !=0){
                bytesString[charCount] = char;
                charCount++;
            }
        }

        bytes memory bytesStringTrimmed = new bytes(charCount);
        for(j=0;j<charCount;j++){
            bytesStringTrimmed[j]=bytesString[j];
        }
        return string(bytesStringTrimmed);
        
    }
    
    // 事件函数
    event Log(string val);

        
    function update1(uint index,string  memory  value) public{

        edb[index]=link;
        edb[index].addNode(strTobytes32(value));
        
    }
    
    function update2(uint index,string  memory  value) public{

        edb[index].addNode(strTobytes32(value));
        
    }
    
    function search(uint index) public {
        
        bytes32 i = edb[index].iterate_start();   
      	while(edb[index].can_iterate(i)){            
      		emit Log(bytes32Tostr(i));           
       		i = edb[index].iterate_next(i);
      	}
    }

}
