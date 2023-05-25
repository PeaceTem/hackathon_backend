const formBx = document.getElementById('registration-form');
const nameField = document.getElementById('username');
const email = document.getElementById('email');
const password = document.getElementById('password');
const nameError = document.getElementById('name-error');
const emailError = document.getElementById('email-error');
const passwordError = document.getElementById('password-error');


nameError.style.display = 'none';
emailError.style.display = 'none';
passwordError.style.display = 'none';

formBx.addEventListener( 'submit', function(e) {
    e.preventDefault(); 
    userFormValidation()
})

nameField.addEventListener('keyup', () =>{
    nameValidation();
})

email.addEventListener('keyup', ()=>{
    emailValidation();
})

password.addEventListener('keyup', ()=>{
    passwordValidation();
})

function userFormValidation() {
    
    if(!nameValidation()  && !emailValidation() && !passwordValidation())
        return;

    formBx.submit();
}

const nameValidation = ()=>{

    
    if (nameField.value.trim() === ''){
        nameError.textContent = "Name cannot be empty";
        nameError.style.display = 'block';
        return false;
      } else {
        nameError.textContent = "";
        nameError.style.display = 'none';
        
        if (nameField.value.trim().length < 1 || nameField.value.trim().length > 30) {
          nameError.textContent = "The username must be between 1 to 30 letters long"; // Set error message text
        nameError.style.display = 'block';
          
          return false;
        } else {
          nameError.textContent = ""; // Set error message text
        nameError.style.display = 'none';

        }
  
      }
      return true;
  
}
// nameValidation();

const emailValidation = ()=>{

    if (email.value.trim() === ''){
        emailError.textContent = "Email cannot be empty";
        emailError.style.display ='block';
        return false;
      } else {
        emailError.textContent = "";
        emailError.style.display ='none';

      }
      return true;
  
}
// emailValidation();

const passwordValidation = ()=>{

    
    if (password.value.trim() === ''){
        passwordError.textContent = "Password cannot be empty";
        passwordError.style.display = "block";
        return false;
      } else {
        passwordError.textContent = "";
        if (password.value.trim().length < 8 || password.value.trim().length > 20) {
          passwordError.textContent = "The password must be between 8 to 20 letters long"; // Set error message text
          passwordError.style.display = "block";

          return false;
        } else {
          passwordError.textContent = ""; 
          passwordError.style.display = "none";

        }
        
      }
      return true;
}
// passwordValidation();
