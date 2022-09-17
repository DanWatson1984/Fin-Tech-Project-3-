import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import numpy as np

load_dotenv()

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
st.title("Sell Home and Issue Title")
accounts = w3.eth.accounts
# Use a streamlit component to get the address of the artwork owner from the user
address = st.selectbox("Select City Address", options=accounts)
seller = st.selectbox("Select Seller", options=accounts)
buyer = st.selectbox("Select Buyer", options=accounts)
bank = st.selectbox("Select Bank", options=accounts)
taxId=st.text_input("Enter Tax ID")
# Use a streamlit component to get the artwork's URI
home_uri = st.text_input("The URI to the Home")
sell_price= st.text_input("Price in ETH","0")
intSellPrice=int (sell_price)
if st.button("Register Home for Sale"):

    # Use the contract to send a transaction to the registerArtwork function
    tx_hash = contract.functions.registerHome(
        seller, buyer, bank, taxId,intSellPrice,home_uri, home_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

st.markdown("---")

################################################################################
# Display a Token
################################################################################
st.markdown("## Display an Home Title Token")

selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address owns {tokens} tokens")

token_id = st.selectbox("Home Title Tokens", list(range(tokens)))

if st.button("Display"):

    # Use the contract's `ownerOf` function to get the Home Title token owner
    owner = contract.functions.ownerOf(token_id).call()
    information = contract.functions.homeTitles(token_id).call()
    st.write(f"{information}")
    st.write(f"The token is registered to {owner}")
    st.write(f"Tax Id {information[3]}")
    st.write(f"Price {information[4]} ETH")
    st.write(f"Mortgage Holding Bank {information[2]}")
    st.write(f"Current Lien Amount  {information[5]} ETH")
    # Use the contract's `tokenURI` function to get the Home Title token's URI
    token_uri = contract.functions.tokenURI(token_id).call()
    if not token_uri:
        tokn_url="No URI was provided"
    else:
        st.write(f"The tokenURI is {token_uri}")
        st.image(token_uri)
    
 ################################################################################
# Put a Lien on the Home Title
################################################################################  
accounts2 = w3.eth.accounts
st.markdown("## Put a Lien on the Home Title")
lienAmount=st.text_input("Enter Lien Amount in ETH")
bank_address=st.selectbox("Bank Address", options=accounts2)
owner_address = st.selectbox("Owner Address", options=accounts2)
tokens2 = contract.functions.balanceOf(owner_address).call()

token_id_4_lien = st.selectbox("Home Title Token", list(range(tokens2)))

if st.button("Register Lien"):
   
    tx_hash2 = contract.functions.putA_Lien(
        int(lienAmount), token_id_4_lien,bank_address
    ).transact({"from": w3.eth.accounts[0]})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash2)
    st.write(receipt)
st.markdown("---")

