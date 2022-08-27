function FirstLoad(){
    if(localStorage.getItem("first") == null){
        var localDate = new Date();
        localStorage.setItem("date", localDate);
        localStorage.setItem("first","done");
    }
    setDate();
}

function confirmForm(e){
    if (!confirm("Xác nhận hoàn tất!!!"))
        e.preventDefault();
}

function getDateList(){
    var start = document.querySelector('input[name="date"]');
    var date = new Date(start.value);
    var dd = date.getDate();
    var mm = date.getMonth()+1;
    var yyyy = date.getFullYear();
    if(dd<10){
      dd='0'+dd;
    }
    if(mm<10){
      mm='0'+mm;
    }
    var date1 = yyyy+'-'+mm+'-'+dd;
    document.getElementById("date").value = date1;
    fetch('/update_list');
}

function getCurrentDate(int){
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1;
    var yyyy = today.getFullYear();
    if(dd<10){
      dd='0'+dd;
    }
    if(mm<10){
      mm='0'+mm;
    }
    if (int !=0){
        var mmax = today.getMonth()+2;
        if(mmax<10){
            mmax='0'+mmax;
        }
        today = yyyy+'-'+mmax+'-'+dd;
        return today;}
    today = yyyy+'-'+mm+'-'+dd;
    return today;
}

function getDateMM(){
    var today = getCurrentDate(0);
    document.getElementById("date").value = today;
    document.getElementById("date").setAttribute("min", today);
    document.getElementById("date").setAttribute("max", getCurrentDate(1));
}

function getDate(){
    document.getElementById("date").value = getCurrentDate(0);
}

function saveDate(){
    var start = document.querySelector('input[name="date-exam"]');
    var date = new Date(start.value);
    localStorage.setItem("date", date);
}

function setDate(){
    var date1 = new Date(localStorage.getItem("date"));
    var dd = date1.getDate();
    var mm = date1.getMonth()+1;
    var yyyy = date1.getFullYear();
    if(dd<10){
      dd='0'+dd
    }
    if(mm<10){
      mm='0'+mm
    }
    var date2 = yyyy+'-'+mm+'-'+dd;
    document.getElementById("date-exam").value = date2;
    getDateList();
}

window.globalCounter = 1;

