console.log("heyy");
//check_signup();
function check_signup()
{
    let username = document.getElementById("name").value;
    let passwrd = document.getElementById("password").value;
    let rptPass = document.getElementById("rptPass").value;
    let email = document.getElementById("email").value;

    if(username == "" && passwrd == "" && rptPass == "" && email == "")
    {
        console.log("Enter values");
    }
    else
    {
        if(username.length > 20)
        {
            console.log("choose lesser value");
        }
        else if(passwrd != rptPass && passwrd.length < 6 && passwrd.length > 20)
        {
            console.log("enter correct password");
        }
        else
        {
            console.log("error");
        }

    }

}


function menu_check()
{
    let itemName = document.getElementById("itemname");
    let itemPrice = document.getElementById("itemprice");

    if(itemName == "" && itemPrice == "")
    {
        console.log("enter menu values");
    }
}

function login_check()
{
    let username = document.getElementById("user").value;
    let passwrd = document.getElementById("pass").value;

    if(username == "" && passwrd == "")
    {
        console.log("Empty Fields Not allowed");
    }
}

function resetPass()
{
    let pass1 = document.getElementById("newPass").value;
    let passConfrm = document.getElementById("cnfrmPass").value;

    if (pass1 != passConfrm)
    {
        console.log("Password Mismatch");
    }
}

function changeMenu()
{
    let name = document.getElementById("itemname");
    let price = document.getElementById("newprice");

    if(name == "" && price == "")
    {
        console.log("Empty fields not allowed")
    }
}

function changePass()
{
    let old = document.getElementById("oldpswd");
    let newp = document.getElementById("newpswd");

    if(old == "" && newp == "")
    {
        console.log("Empty fields not allowed");
    }
    else if(old === newp)
    {
        console.log(" Same passwords not allowed");
    }
}

function userSignup()
{
    console.log("here")
    let username = document.getElementById("name").value;
    let passwrd = document.getElementById("password").value;
    let rptPass = document.getElementById("rptPass").value;
    let email = document.getElementById("email").value;
    let address = document.getElementById("address").value;

    if(username == "" && passwrd == "" && rptPass == "" && email == "" && address == "")
    {
        alert("enter values");
        console.log("Enter values");
    }
    else
    {
        if(username.length > 20)
        {
            alert("enter values");
            console.log("choose lesser value");
        }
        else if(passwrd != rptPass && passwrd.length < 6 && passwrd.length > 20)
        {
            alert("enter values");
            console.log("enter correct password");
        }
        else
        {
            alert("enter values");
            console.log("error");
        }
    }
}
