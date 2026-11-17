
let m=60;
let s=0;
let t;
let isRunning=false;
function updateDisplay(){
    let min=m<10?"0"+m:m;
    let sec=s<10?"0"+s:s;
    document.getElementById("timer").innerText=min+":"+sec;
}
function startTimer()
{
    if(isRunning) return;
    isRunning=true;
    timer=setInterval(function(){
        if(s===0){
            if(m===0){
                clearInterval(timer);
                isRunning=false;
                alert("Time's up! Take a break😊");
                return;
            }
            m--;
            s=59;
        }else{
            s--;
        }
        updateDisplay();
    },1000);
}
function stopTimer(){
    clearInterval(timer);
    isRunning=false;
}
function resetTimer(){
    clearInterval(timer);
    m=60;
    s=0;
    isRunning=false;
    updateDisplay();
}
 function addTask() {
    let input = document.getElementById("taskInput");
    let taskText = input.value.trim();

    if (taskText === "") {
        alert("Please enter a task");
        return;
    }

    let li = document.createElement("li");
    li.innerText = taskText;

    document.getElementById("taskList").appendChild(li);
    input.value = "";
}