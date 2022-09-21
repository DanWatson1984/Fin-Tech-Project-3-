import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
load_dotenv()
st.set_page_config(layout="wide")
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./Compiled/RegisterHomeForSale_abi.json')) as f:
        homeTitle_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS2")

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=homeTitle_abi
    )

    return contract

contract = load_contract()

################################################################################
# Register New HomeTitle
################################################################################
#Registering bootstrap information to use in html
html_code="<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css' integrity='sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm' crossorigin='anonymous'><script src='https://code.jquery.com/jquery-3.2.1.slim.min.js' integrity='sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN' crossorigin='anonymous'></script><script src='https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js' integrity='sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q' crossorigin='anonymous'></script><script src='https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js' integrity='sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl' crossorigin='anonymous'></script><style>button{background-color:#17a2b8 !important;color:white !important;height:70px !important;font-size:2rem !important;line-height:3 !important;}</style>"
st.markdown("<div class='jumbotron' style='background-color:#6610f2 !important;color:white !important;'><h1>FinTech City Home Title System</h1><p>This is the site to issue new home titles and add Liens to the Titles.</p></div>"
,unsafe_allow_html=True )
##Page layout is set to two columns
col1, col2 = st.columns(2)
with col1:       
    st.markdown(html_code, unsafe_allow_html=True)
    st.markdown("<Div role='alert' class='alert alert-primary' ><h1>Sell Home and Issue Title</h1></Div>",unsafe_allow_html=True)
    st.markdown("<h3>The account that belongs to the city of FinTech is</h3><h2 style='color:red;'> 0x79a5Afd814b91C5Fa97f4d4B84Ab9E7D75b4Fa10</h2>", unsafe_allow_html=True)
    accounts = w3.eth.accounts
    # Use a streamlit component to get the address of the related infomation to the home

    address = st.selectbox("Select City Address", options=accounts)
    seller1 = st.selectbox("Select Seller", options=accounts)
    buyer1 = st.selectbox("Select Buyer", options=accounts)
    bank1 = st.selectbox("Select Bank", options=accounts)
    taxId1=st.text_input("Enter Tax ID")
    # Use a streamlit component to get the home URI
    home_uri1 = st.text_input("The URI to the Home")
    sell_price1= st.text_input("Price in ETH","0")
    intSellPrice1=int (sell_price1)
    index =accounts.index(address)
    if st.button("Issue New Home Title"):
            
        # Use the contract to send a transaction to the Title function
        tx_hash = contract.functions.registerHome(
            seller1, buyer1, bank1, taxId1, intSellPrice1,home_uri1
        ).transact({'from': w3.eth.accounts[index], 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        with col2:
            st.write("Transaction receipt mined:")
            st.write(dict(receipt))
            st.write(f"sller {seller1}")
            st.write(f"buyer {buyer1}")
            st.write(f"taxid {taxId1}")
            st.write(f"intSellPrice1 {intSellPrice1}")
            st.write(f"home_uri1 {home_uri1}")
    st.markdown("---")

################################################################################
# Display a Token
################################################################################
with col1:
    st.markdown("<Div role='alert' class='alert alert-success' ><h1>Display Home Title Token</h1></Div>",unsafe_allow_html=True)
    selected_address1 = st.selectbox("Select Account", options=accounts)
    tokens2 = contract.functions.balanceOf(selected_address1).call()
    title_tokenIds = []
    st.write(f"This address owns {tokens2} tokens")
    #token_id2 = st.selectbox("Home Title Tokens", (range(tokens2)))
    for x in range(tokens2):
        tokenID = contract.functions.tokenOfOwnerByIndex(selected_address1, x).call()
        title_tokenIds.append(tokenID)
        #st.write(f"Token ID at {x} -- {tokenID}")
    if len(title_tokenIds)>0:
        token_id2 = st.selectbox("Home Title Tokens", (title_tokenIds))
        information = contract.functions.homeTitleCollection(token_id2).call()
   
    if st.button("Display Information"):

        # Use the contract's `ownerOf` function to get the Home Title token owner
       
        owner2 = contract.functions.ownerOf(token_id2).call()
        
       
        with col2:
            #st.write(f"{tokens2}")
            st.write(f"<div class='alert alert-secondary'  role='alert'><b>The Title owner </b>  {owner2}</div>",unsafe_allow_html=True)
            st.write(f"<div class='alert alert-secondary'  role='alert'><b>Tax Id</b> {information[3]}</div>",unsafe_allow_html=True)
            st.write(f"<div class='alert alert-secondary'  role='alert'><b>Price</b> {information[4]}ETH</div>",unsafe_allow_html=True)
            st.write(f"<div class='alert alert-secondary'  role='alert'><b>Mortgage Holding Bank</b> {information[2]}</div>",unsafe_allow_html=True)
            st.write(f"<div class='alert alert-secondary'  role='alert'><b>Current Lien Amount</b> {information[5]}ETH</div>",unsafe_allow_html=True)
            
            
            # Use the contract's `tokenURI` function to get the Home Title token's URI
           # token_uri = contract.functions.tokenURI(token_id).call()
            image_uri=information[6]
            if not image_uri:
                tokn_url="No URI was provided"
            else:
                
                st.image(image_uri)
        
 ################################################################################
# Put a Lien on the Home Title
################################################################################  
accounts2 = w3.eth.accounts
with col1:
    st.markdown("<Div role='alert' class='alert alert-danger' ><h1>Put a Lien on a Home</h1></Div>",unsafe_allow_html=True)
    city_address = st.selectbox("City Address", options=accounts)
    bank_address=st.selectbox("Bank Address", options=accounts2)
    owner_address3 = st.selectbox("Select Owner Address", options=accounts2)
    tokens2 = contract.functions.balanceOf(owner_address3).call()
    cityindex =accounts.index(city_address)
    title_tokenIds2 = []
    ##################################
    for x in range(tokens2):
        tokenID2 = contract.functions.tokenOfOwnerByIndex(owner_address3, x).call()
        title_tokenIds2.append(tokenID2)
        #st.write(f"Token ID at {x} -- {tokenID}")
    token_id_4_lien = st.selectbox("Home Title Tokens - For Lien", (title_tokenIds2))
    #################################
    lienAmount=st.text_input("Enter Lien Amount in ETH")

    #token_id_4_lien = st.selectbox("Home Title Token", list(range(tokens2)))

    if st.button("Register Lien on Property"):
    
        tx_hash2 = contract.functions.putA_Lien(
            int(lienAmount), token_id_4_lien,bank_address
        ).transact({"from": w3.eth.accounts[cityindex]})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash2)
        st.write(receipt)
st.markdown("---")


################################################################################
# Transfer Existing Title to New Owner - Home Resale
################################################################################  
accounts2 = w3.eth.accounts
with col1:
    st.markdown("<Div role='alert' class='alert alert-warning' ><h1>Transfer Existing Title to New Owner</h1></Div>",unsafe_allow_html=True)
    saleExecutor = st.selectbox("Sale Executed By:", options=accounts2)
    seller_address = st.selectbox("Seller Address", options=accounts2)
    buyer_address = st.selectbox("Buyer Address", options=accounts2)
    newBank_address = st.selectbox("New Bank Address", options=accounts2)
    seller_token = contract.functions.balanceOf(seller_address).call()
   
    token_to_be_resold = st.selectbox("Home Title Token:", list(range(seller_token)))
    #newSell_price= st.text_input("New Sale Price:","0")
    #intSellPriceNew=int (newSell_price)
    index =accounts2.index(seller_address)
     ###In order to sell the property the city account has been granted access to to transfer the tokens
    contract.functions.setApprovalForAll(accounts[1], True).transact({"from": w3.eth.accounts[index]})
    if st.button("Resell and Update Title"):
       
        
        ##Title can be transferred by the owner or the city address 0x79a5Afd814b91C5Fa97f4d4B84Ab9E7D75b4Fa10

        tx_hash_transfer=contract.functions.transferFrom(seller_address, buyer_address,int(token_to_be_resold)).transact({"from": w3.eth.accounts[index]})
        receipt_transfer = w3.eth.waitForTransactionReceipt(tx_hash_transfer)
        st.markdown(receipt_transfer)
        st.markdown("---")
