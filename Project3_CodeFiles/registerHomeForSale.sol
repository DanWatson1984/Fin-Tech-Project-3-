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
    }

    mapping(uint256 => HomeTitle) public homeTitles;
    event RegisterHomeForSale(address seller, address buyer, address bank, uint256 token_id, uint256 newPrice, string taxId, string reportURI);

    function registerHome(
        address seller,
        address buyer,
        address bank,
        string memory taxId,
        uint256 sellPrice,
        string memory tokenURI
       
) public returns (uint256) {

     uint256 tokenId = totalSupply();

        _mint(seller, tokenId);
        _setTokenURI(tokenId, tokenURI);

        homeTitles[tokenId] = HomeTitle( seller, buyer, bank, taxId, sellPrice);

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

        emit RegisterHomeForSale(seller, buyer, bank,tokenId, newPrice, taxId, reportURI_);

        return homeTitles[tokenId].sellPrice;
    }
}