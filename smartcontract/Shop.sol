// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.7;

contract Shop {
    address owner;
    enum ItemStatus{Sold, Available}

    mapping (address => uint256) balanceOf; 

    struct Item {
        uint itemId;
        string title;
        uint price;
        ItemStatus status;
    }

    Item[] items;

    uint id_sequence;

    constructor() {
        owner = msg.sender;
        initItems();
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function pushItem(string memory title, uint price) internal {
        items.push(Item(id_sequence++, title, price, ItemStatus.Available));
    }

    function initItems() internal {
        pushItem("Apple", 1);
        pushItem("Banana", 2);
        pushItem("Orange", 3);
    }
    

    function getItems() public view returns(Item[] memory) {
        return items;
    }

    function addItem(string memory title, uint price) external onlyOwner {
        pushItem(title, price);
    }


    function sellAll() external onlyOwner {
        for(uint i = 0; i < items.length; i++) {
            items[i].status = ItemStatus.Sold;
        }
    }

    function buyItem(uint id) external payable {
        for(uint i = 0; i < items.length; i++) {
            if(items[i].itemId == id) {
                require(items[i].status == ItemStatus.Available);
                require(balanceOf[address(this)] >= items[i].price);
                items[i].status = ItemStatus.Sold;
                balanceOf[address(this)] -= items[i].price;
                return;
            }
        }
    }

    function sellItem(uint itemId) external payable onlyOwner {
        for (uint i = 0; i < items.length; i++) {
            Item memory currItem = items[i];

            if (currItem.itemId == itemId) {
                require(currItem.status == ItemStatus.Available, "Item is not available.");
                items[i].status = ItemStatus.Sold;
                balanceOf[address(this)] += items[i].price;
                return;
            }
        }

        revert("There is no item with such id.");
    }


    function getItem(uint itemId) public view returns(Item memory) {
        for (uint i = 0; i < items.length; i++) {
            Item memory currItem = items[i];

            if (currItem.itemId == itemId) {
                return currItem;
            }
        }

        revert("There is no item with such id.");
    }

    function getItemStatus(uint itemId) public view returns(ItemStatus) {
        return getItem(itemId).status;
    }

    function getItemPrice(uint itemId) public view returns(uint) {
        return getItem(itemId).price;
    }

    function getItemTitle(uint itemId) public view returns(string memory) {
        return getItem(itemId).title;
    }


    function getItemId(uint itemId) public view returns(uint) {
        return getItem(itemId).itemId;
    }

    function getBalance() public view returns(uint) {
        return balanceOf[address(this)];
    }

    function getOwner() public view returns(address) {
        return owner;
    }

    function getItemsCount() public view returns(uint) {
        return items.length;
    }

}

