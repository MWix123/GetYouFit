
function updateForm(elem){
	//var counter = 0;
	
	document.getElementById('id_textarea').textContent = document.getElementById('username').value + ";" + document.getElementById('password').value;
	
	var counter = getSemiColonons();
	/*var textarea = document.getElementById('id_textarea').textContent;
	console.log(textarea);
	for(var i = 0; i < textarea.length; i++){
		if(textarea[i] == ";"){
			counter++;
		}

	}*/

	//console.log(counter);
	if(counter > 1){
		document.getElementById("login-error-message").innerHTML = "The character ';' is not allowed.";
		//elem.value = elem.value.substr(0, elem.value.length-1);
	}else{
		document.getElementById("login-error-message").innerHTML = "";
	//	document.getElementById('id_textarea').textContent = document.getElementById('username').value + ";" + document.getElementById('password').value;
	}
}

function validateLogin(){
	//alert("started");
	//console.log("here!!!!!!!!!!!!!!");
	var textarea = document.getElementById('textarea');
	//alert("whet: " + getSemiColonons());
	if(getSemiColonons() > 1){
		//alert("not subnitted");
		return false;
	}else{
		//alert("submitted");
	}
}

function getSemiColonons(){
	var counter = 0;
	var textarea = document.getElementById('id_textarea').textContent;
	console.log(textarea);
	for(var i = 0; i < textarea.length; i++){
		if(textarea[i] == ";"){
			counter++;
		}

	}
	return counter;
}
