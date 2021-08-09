var userFormData = {
				'name':null,
				'email':null,
				'total':total,
			}

			var shippingInfo = {
				'address':null,
				'city':null,
			}

		
			shippingInfo.address = form.address.value
			shippingInfo.city = form.city.value

	    	if (user == 'AnonymousUser'){
	    		userFormData.name = form.name.value
	    		userFormData.email = form.email.value
	    	}

	    	console.log('Shipping Info:', shippingInfo)
	    	console.log('User Info:', userFormData)

	    	var url = "/process_order/"
	    	fetch(url, {
	    		method:'POST',
	    		headers:{
	    			'Content-Type':'applicaiton/json',
	    			'X-CSRFToken':csrftoken,
	    		}, 
	    		body:JSON.stringify({'form':userFormData, 'shipping':shippingInfo}),
	    		
	    	})
	    	.then((response) => response.json())
	    	.then((data) => {
				console.log('Success:', data);
				alert('Order completed');  
				//cart = {}
				//document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

				window.location.href = "{% url 'products' %}"

				})