editButtonActive = false;
prevFood = "";
prevCalorie = "";
entryDate = "";

function init(){

	if(document.getElementById('id_typeForm_0').checked){
		updateVisibleForm("block","none","none", "inline");	
	}else{
		updateVisibleForm("none","block","inline", "none");

	}

	var elems = document.getElementsByName('typeForm');
	for(var i = 0; i < elems.length; i++){
		elems[i].addEventListener("change", function(event) {
			if(this.value == "Strength"){
				updateVisibleForm("block","none","none", "inline");
			}else{
				updateVisibleForm("none","block","inline", "none");
			}
		});
	}


	var duration = document.getElementById('id_duration');
	
	duration.addEventListener("keyup", function(event){
		if(isNaN(this.value[this.value.length-1]) && this.value[this.value.length-1] != ':'){
			this.value = this.value.substring(0, this.value.length-1);
		}
	});
}

function validate(){
	if(document.getElementById('id_typeForm_1').checked){
		var duration = document.getElementById('id_duration');

		var index1 = duration.value.indexOf(":");
		var index2 = duration.value.indexOf(":", index1+1);
		var length = duration.value.length;

		//alert("index1: " + index1 + " index2: " + index2 + " index3: " + (length-1));
		//alert(duration.value.substring(index1+1,index2));
		//alert(duration.value.substring(index2+1,length));
		if(duration.value.substring(index1+1,index2).length > 2 || duration.value.substring(index2+1,length).length > 2){
			document.getElementById("login-error-message").innerHTML = "Error: duration field not properly formatted.";
			return false;
		}
	}

	return true;
}

function updateVisibleForm(style1,style2,style3, style4){
	document.getElementById('id_muscle').style.display = style1;
	document.getElementById('id_weight').style.display = style1;
	document.getElementById('id_repetitions').style.display = style1;
	document.getElementById('id_duration').style.display = style2;
	document.getElementById('id_distance').style.display = style2;


	var labels = document.getElementsByTagName("label");
	for(var j = 0; j < labels.length; j++){
		switch(labels[j].htmlFor){
			case "id_muscle":
			case "id_weight":
			case "id_repetitions":
				labels[j].style.display = style4;
				break;
			case "id_duration":
			case "id_distance":
				labels[j].style.display = style3;
				break;
			default:
				break;
		}
	}

	document.getElementsByClassName("helptext")[0].style.display  = style1;
	document.getElementsByClassName("helptext")[1].style.display  = style2;
}











function initEntries(){
	var closeButtons = document.getElementsByClassName('close-button');
	var editButtons = document.getElementsByClassName('edit-button');

	for(var i = 0; i < closeButtons.length; i++){
		closeButtons[i].addEventListener("click", function(event){
			//clearAllEditable();


			if(this.parentNode.className == "Diet-Entry"){
				entryDate = this.parentNode.children[1].innerHTML;
				entryDate = entryDate.substring(12, 16) + "-" 
							+ entryDate.substring(6, 8) + "-" 
							+ entryDate.substring(9, 11);
				document.getElementById('id_single_0').checked = "true";
				document.getElementById('id_date3').value = entryDate;
				document.getElementById('id_food3').value = "a";
				document.getElementById('id_calories3').value = 1;

				document.getElementById("delete-form").submit();
				//alert("Delet day");
			}else if(this.parentNode.className == "Diet-Sub-Entry"){
				entryDate = this.parentNode.parentNode.children[1].innerHTML;
				entryDate = entryDate.substring(12, 16) + "-" 
							+ entryDate.substring(6, 8) + "-" 
							+ entryDate.substring(9, 11);
				document.getElementById('id_single_1').checked = "true";
				document.getElementById('id_date3').value = entryDate;
				document.getElementById('id_food3').value = this.parentNode.children[2].children[0].innerHTML;
				document.getElementById('id_calories3').value = this.parentNode.children[3].children[0].innerHTML;
				
				document.getElementById("delete-form").submit();
				//alert("Delet item");
			}
		});
	}

	for(var i = 0; i < editButtons.length; i++){
		editButtons[i].addEventListener("click", function(event){
			clearAllEditable();

			makeEditable(this.parentNode.children[2].children[0]);
			makeEditable(this.parentNode.children[3].children[0]);

			entryDate = this.parentNode.parentNode.children[1].innerHTML;
			entryDate = entryDate.substring(12, 16) + "-" 
						+ entryDate.substring(6, 8) + "-" 
						+ entryDate.substring(9, 11);
						
			prevFood = this.parentNode.children[2].children[0].innerHTML;
			prevCalorie = this.parentNode.children[3].children[0].innerHTML;

			
			if(!editButtonActive){
				var mainElem = document.getElementsByClassName('main');
				var newButton = document.createElement("input");
				newButton.setAttribute("type", "button");
				newButton.setAttribute("value", "Update");
				newButton.id = "edit-submit";
				newButton.addEventListener("click", function(event){
					document.getElementById("id_date").value = entryDate;
					document.getElementById("id_food").value = document.getElementsByClassName("focused")[0].innerHTML;
					document.getElementById("id_calories").value = document.getElementsByClassName("focused")[1].innerHTML;
				
					document.getElementById("id_food2").value = prevFood;
					document.getElementById("id_calories2").value = prevCalorie;
					
					document.getElementById("edit-form").submit();
				});
				mainElem[0].appendChild(newButton);
				
				editButtonActive = true;
			}
		});
	}


	//document.querySelectorAll("[id='id_date']")[1].id = "id_date2";
	//document.querySelectorAll("[id='id_food']")[1].id = "id_food2";
	//document.querySelectorAll("[id='id_calories']")[1].id = "id_calories2";
}

function makeEditable(elem){
	elem.contentEditable = "true";
	elem.className = "editable focused";	
}

function clearAllEditable(){
	var editables = document.getElementsByClassName('editable');
	var counter = 0;
	for(var i = 0; i < editables.length; i++){
		if(editables[i].className == "editable focused"){
			if(counter == 0){
				editables[i].innerHTML = prevFood;
			}else{
				editables[i].innerHTML = prevCalorie;
			}
			counter++;

		}
		editables[i].className = "editable";
		editables[i].contentEditable = "false";
	}
}