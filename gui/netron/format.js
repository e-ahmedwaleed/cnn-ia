this.__view__.toggle("names");


this.document.getElementById("toolbar").remove();
this.document.getElementById("edge-labels").remove();
this.document.getElementById("nodes").style.pointerEvents = "none";

this.__view__.export(document.title + ".png")
