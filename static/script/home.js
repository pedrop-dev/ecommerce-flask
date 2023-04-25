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