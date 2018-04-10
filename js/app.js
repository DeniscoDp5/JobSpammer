
function listResults(input) {
	var el = $("#list-Area").css("display", "inherit")
	el.css("width", "100%")
	for (i = 0; i < input.length; i++) {
		var p = document.createElement("p");
		p.className = "p.element-in-list ";
		p.innerHTML = (i + 1) + " " + input[i]
		if (i % 2 == 0) {
			p.classList.add("ligther");
		}
		el.append(p)

	}
}
/** 
advanceStatus = function (i) {
	if (i == 1) {
		$("#informer").html("Stiamo Processando la Richiesta")
		$(".progress-bar").css("width", "10%")
		setTimeout(function () { advanceStatus(2) }, 4000);
	} else if (i == 2) {
		$("#informer").html("Recupero Dei contatti online")
		$(".progress-bar").css("width", "15%")
		setTimeout(function () { advanceStatus(3) }, 8000);
	} else if (i == 3) {
		$("#informer").html("Attendi per favore")
		$(".progress-bar").css("width", "25%")
		$("#loader").css("display", "inline-block")
	}
}
*/
var response1;
var response2 = []
var officilResponse2 = [];
var officilResponse3 = [];
$('#button').click(function () {
	
	classList = $('#button').attr("class");
	cat = $("#category").val();
	loc = $("#location").val()
	if (cat == "Seleziona La Categoria" || loc == "Seleziona la Localita'") {
		return
	}else{
		$(".progress").css("display","flex")
	}
	$("#informer").html("Stiamo elaborando la tua richiesta. Potrebbero volerci alcuni minuti");
	$("#button").css("display", "none");
	$(".progress-bar").css("width", "5%");
	$("#loader").css("display", "inline-block");
	$("#form-container").css("display","none");
	$.ajax({
		url: "cgi-bin/downloader.py",
		
		data: { category: cat, location: loc },
		contentType: "json",
		dataType: "json",
		//type:"post",
		success: function (json) {
			$(".progress-bar").css("width", "33%");
			$("#informer").html("Rimozione dei dati duplicati");
			
			response1 = removeDuplicates(json.response)
			listResults(response1);
			$(".progress-bar").css("width", "50%");
			$("#loader").css("display", "none");
			$("#informer").attr("class","col-12");
			$("#informer").html("Prima fase completata con successo");
			$("#button-2").css("display","block");
		},
		error: function () {
			$(".progress-bar").css("width", "0%");
			$("#informer").html("Errore");
		}
	})
});

function removeDuplicates(inp){
	l = inp.length;
	resul = [];
	resul[0] = inp[0];
	for(i = 1;i< l;i++){
		boole = false
		for(j=0;j<resul.length & !boole ;j++){
			if(resul[j] == inp[i]){
				boole = true;
			}
		}
		if(boole == false){
			resul.push(inp[i])
		}
	}
	return resul; 
	
}

/**
 * Seconda fase del processo
 * 
 */

 $("#button-2").click(
	 function(){
		 $("#button-2").css("display","none");
		 me = this;
		 $("#informer").html("Attendi per favore");
		this.response = arrangeArray(response1);
		$("#informer").html("Seconda fase iniziata con successo");
		for(i=0;i<this.response.length;i++){
			sleep(5000);
			this.data = JSON.stringify(this.response[i]);
			$.ajax({
				//contentType: "json",
				//dataType: "json",
				url: "cgi-bin/googleFinder.py",
				data : {'array' : this.data},
				success : function(json){
					response2.push(JSON.parse(json).response);
					w = $(".progress-bar").css("width"); // TODO: Arrivati a questo punto bisogna migliorare l'avanzamento della progress-bar. Gestire in maniera ordinata i dati ricevuti dalle response. Migliorare interfaccia grafica della seconda fase. Fare la ricerca web con gli indirizzi web trovati e cercare un email  
					$(".progress-bar").css("width",parseInt(w)+10);
					$("#informer").html("completamento delle operazioni in corso");
					if(me.response.length == response2.length){
						renderFaseTwo();
					}
				},
				error : function(){
					alert("error")
				}
			});
		}
		}
 );

function arrangeArray(arIN) {
	this.result = [];
	l = arIN.length
	q = parseInt(l / 20);
	r = l % 20;
	for (i = 0; i < q; i++) {
		this.result[i] = []
		for (j = 0; j < 20; j++) {
			this.result[i][j] = arIN[i * 20 + j];
		}
	}
	this.result[q] = [];
	for (i = 0; i < r; i++) {
		this.result[q][i] = arIN[q * 20 + i];
	}
	return this.result;
}

function sleep(milliseconds) {
	var start = new Date().getTime();
	for (var i = 0; true; i++) {
	  if ((new Date().getTime() - start) > milliseconds){
		break;
	  }
	}
  }
function renderFaseTwo(){
	this.response = response2;

	$("#informer").html("Visualizzazione dei dati")
	var el = $("#list-Area")
	el.html("");
	count = 1
	for (i = 0; i < this.response.length; i++) {
		for(j=0;j<this.response[i].length;j++){
			var p = document.createElement("p");
			p.className = "p.element-in-list ";
			p.innerHTML = (count) + " " + this.response[i][j];
			count ++;
			el.append(p);
			officilResponse2.push(this.response[i][j])
		}
	}
	$("#informer").html("Seconda fase completata")
	$("#button-3").css("display","inline");
}

$("#button-3").click(	// fase tre 
	function(){
		$("#button-3").css("display","none");
		$("#informer").html("Inizio della terza fase");
		me = this;
		me.error = 0
		this.res = officilResponse3;
		this.inARR = arrangeArray(officilResponse2);
		for (i = 0; i < this.inARR.length; i++) {
			this.data = JSON.stringify(this.inARR[i]);
			sleep(500);	
			$.ajax({
				//contentType: "json",
				//dataType: "json",
				type: "post",
				url: "cgi-bin/EmailFinder.py",
				data: { 'array': this.data },
				success: function (json) {
					$("#informer").html("Completamento della terza fase");
					me.res.push(JSON.parse(json).response);
					//w = $(".progress-bar").css("width","80%"); // TODO: Arrivati a questo punto bisogna migliorare l'avanzamento della progress-bar. Gestire in maniera ordinata i dati ricevuti dalle response. Migliorare interfaccia grafica della seconda fase. Fare la ricerca web con gli indirizzi web trovati e cercare un email  
					if(me.error + me.res.length == me.inARR.length){
						$("#informer").html("ELENCO EMAIL COMPLETO");
						officilResponse3 =  removeDuplicates( renderFaseThree(me.res));
						displayResults(officilResponse3);
					}
				},
				error: function () {
					me.error = me.error + 1;
				}
			});
		}
	}
); 
function renderFaseThree(inArray){
	this.temp = [];
	for(i = 0; i<inArray.length;i++){
		for(j=0;j<inArray[i].length;j++){
			this.temp.push(inArray[i][j])
		}
	}
	return this.temp;
}

function displayResults(inArray){
	var el = $("#list-Area");
	el.html("");
	for(i=0 ; i< inArray.length;i++){
		var p = document.createElement("p");
		p.className = "p.element-in-list ";
		p.innerHTML = (i) + " " + inArray[i];
		el.append(p);
	}
}