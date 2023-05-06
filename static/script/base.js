function showMenu() {
    navBar = document.querySelector(".nav-bar");
    navBar.classList.toggle("active");
}

//Cart

function openCart() {
    const cartDisapear = document.querySelector('#cart-disapear')
    const menuAccountDisappear = document.querySelector('#account-menu-disappear')

    //Cart appear
    cartDisapear.style.display = 'block'
    //Menu disappear
    menuAccountDisappear.style.display = 'none'
}

function closeCart() {  
    const cartDisapear = document.querySelector('#cart-disapear')
    cartDisapear.style.display = 'none'
}

function addToCart() {
    const cartItems = document.querySelector(".cart-items")

    
}

//Menu

function openAccountMenu() {
    const menuAccountDisappear = document.querySelector('#account-menu-disappear')
    const cartDisapear = document.querySelector('#cart-disapear')
    
    //Menu appear
    menuAccountDisappear.style.display = 'block'
    //Cart disappear
    cartDisapear.style.display = 'none'
}

function closeAccountMenu() {
    const menuAccountDisappear = document.querySelector('#account-menu-disappear')
    menuAccountDisappear.style.display = 'none'
}
