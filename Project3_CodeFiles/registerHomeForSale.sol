pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract RegisterHome is ERC721Full {
    constructor() public ERC721Full("RegisterHomeForSale", "HMTITLE")  {}

    struct HomeTitle {
       
        address seller;
        address buyer;
        address bank;
        string taxId;
        uint256 sellPrice;
        uint256 lienAmount;
        string reportURI;
    }

    mapping(uint256 => HomeTitle) public homeTitles;
    event RegisterHomeForSale(address seller, address buyer, address bank, uint256 token_id, uint256 newPrice, string taxId, string reportURI,uint256 lienAmount);
    event Lien(address bank, uint256 token_id, uint256 LienAmount);
    function registerHome(
        address seller,
        address buyer,
        address bank,
        string memory taxId,
        uint256 sellPrice,
        string memory tokenURI,
        string memory propertyURI
       
       
) public returns (uint256) {

     uint256 tokenId = totalSupply();

        _mint(buyer, tokenId);
        _setTokenURI(tokenId, tokenURI);

        homeTitles[tokenId] = HomeTitle( seller, buyer, bank, taxId, sellPrice,0,propertyURI);

        return tokenId;

}
function newHomeSaleSubmission(
        uint256 tokenId,
        address seller,
        address buyer,
        address bank,
        string memory taxId,
        string memory reportURI_,
        uint256 newPrice
    ) public returns (uint256) {
        homeTitles[tokenId].sellPrice = newPrice;

        emit RegisterHomeForSale(seller, buyer, bank,tokenId, newPrice, taxId, reportURI_,0);

        return homeTitles[tokenId].sellPrice;
    }

    function putA_Lien(
       
        uint256 newLienAmount,
        uint256 tokenId,
        address bank
       
    ) public returns (uint256) {
        homeTitles[tokenId].lienAmount = newLienAmount;

        emit Lien(bank, tokenId, newLienAmount);

        return homeTitles[tokenId].lienAmount;
    }
}