
function updateForm(elem){
	
	document.getElementById('id_textarea').textContent = document.getElementById('username').value + ";" + document.getElementById('password').value;
	
	var counter = getSemiColonons();

	if(counter > 1){
		document.getElementById("login-error-message").innerHTML = "The character ';' is not allowed.";
	}else{
		document.getElementById("login-error-message").innerHTML = "";
	}
}

function validateLogin(){
	var textarea = document.getElementById('textarea');
	
	if(getSemiColonons() > 1){
		return false;
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
