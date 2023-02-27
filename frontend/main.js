window.addEventListener('DOMContentLoaded' , (event) =>{
    getVisitCount();
})

const functionApiURL = "https://counterfunc.azurewebsites.net/api/HttpTriggerCounter2"
const functionApiLocal  = 'http://localhost:7071/api/HttpTriggerCounter2';
const getVisitCount = () => {
    let count = 30;
    fetch(functionApiURL).then(response => {
        return response.json()
        //return response
    }).then(response =>{
        console.log("Website called function API.");
        console.log(response);
        //count = response.count;
        count = response
        document.getElementById("counter").innerText = count;
    }).catch(function(error){
        console.log(error);
    });
    return count;
}