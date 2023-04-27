function showMenu() {
    navBar = document.querySelector(".nav-bar");
    navBar.classList.toggle("active");
}

//Cart

function openCart() {
    const cartDisapear = document.querySelector('#cart-disapear')
    //const cartItems = document.querySelector('.cart-items')

    cartDisapear.style.display = 'block'
    //cartItems.style.display = 'block'
}

function closeCart() {  
    const cartDisapear = document.querySelector('#cart-disapear')
    cartDisapear.style.display = 'none'
}

function openAccountMenu() {
    const menuAccountDisappear = document.querySelector('#account-menu-disappear')
    menuAccountDisappear.style.display = 'block'
}

function closeAccountMenu() {
    const menuAccountDisappear = document.querySelector('#account-menu-disappear')
    menuAccountDisappear.style.display = 'none'
}
