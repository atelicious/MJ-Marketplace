var update_btns = document.getElementsByClassName('update-cart')

for (i = 0; i < update_btns.length; i++) {
    update_btns[i].addEventListener('click', function(){
        var product_id = this.dataset.product
        var action = this.dataset.action
        console.log('product_id:', product_id, 'action:', action)

        if (user == 'AnonymousUser'){
            console.log('User is not logged in')
            window.alert('You need to logged in to use the add to cart function')
            
        } else {
            update_user_order(product_id, action)
        }

    })
}


function update_user_order(product_id, action){
    var item_url = '/update_item/'

    fetch(item_url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'product_id':product_id, 'action':action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()
    })

}

