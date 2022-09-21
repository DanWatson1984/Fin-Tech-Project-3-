pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract RegisterHome is ERC721Full {
    constructor() public ERC721Full("HomeTitle", "HMTITLE")  {}
    address city =msg.sender;
    struct HomeTitle {
       
        address seller;
        address buyer;
        address bank;
        string taxId;
        uint256 sellPrice;
        uint256 lienAmount;
        string reportURI;
    }
    
    mapping(uint256 => HomeTitle) public homeTitleCollection;
    event RegisterHomeForSale(uint256 token_id, address seller, address buyer, address bank, uint256 newPrice, string taxId, string reportURI,uint256 lienAmount);
    event Lien(address bank, uint256 token_id, uint256 LienAmount);
    function registerHome(
        address seller,
        address buyer_owner,
        address bank,
        string memory taxId,
        uint256 sellPrice,
        string memory propertyURI
       
       
) public returns (uint256) {
    require(msg.sender==city,"Token can only be issued by the City Account");
     uint256 tokenId = totalSupply();

        _mint(buyer_owner, tokenId);
        _setTokenURI(tokenId, propertyURI);

        homeTitleCollection[tokenId] = HomeTitle( seller, buyer_owner, bank, taxId, sellPrice,0,propertyURI);

        return tokenId;

}
function newHomeSaleSubmission(
        uint256 tokenId,
        address seller,
        address NewBuyer,
        address bank,
        string memory taxId,
        string memory reportURI_,
        uint256 newPrice
    ) public returns (address) {
        homeTitleCollection[tokenId].buyer = NewBuyer;
        
      
    
        emit RegisterHomeForSale(tokenId, seller, NewBuyer, bank, newPrice, taxId, reportURI_,0);
       
        return homeTitleCollection[tokenId].buyer;
        
    }

    function putA_Lien(
       
        uint256 newLienAmount,
        uint256 tokenId,
        address bank
       
    ) public returns (uint256) {
        require(msg.sender==city,"Unauthorized User");
        homeTitleCollection[tokenId].lienAmount = newLienAmount;

        emit Lien(bank, tokenId, newLienAmount);

        return homeTitleCollection[tokenId].lienAmount;
    }

    function getTokenIds(address _owner) public view returns (uint[] memory) {
        uint[] memory _tokensOfOwner = new uint[](ERC721.balanceOf(_owner));
        uint i;

        for (i=0;i<ERC721.balanceOf(_owner);i++){
            _tokensOfOwner[i] = ERC721Enumerable.tokenOfOwnerByIndex(_owner, i);
        }
        return (_tokensOfOwner);
    }
}