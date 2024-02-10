<script setup lang="ts">
import { onMounted, ref } from 'vue';
// Много-много переменных
let register_name = ref("")
let register_email = ref("")
let register_pass = ref("")
let register_submit = ref("")
let register_success = ref("")
let register_failed = ref("")
let login_email = ref("")
let login_pass = ref("")
let nullInputsRegister = ref(false)
let nullInputsLogin = ref(false)
let WhichWarningIsVisibleRegister = ref(null)
let WhichWarningIsVisibleLogin = ref(null)

let serverUrl = 'http://127.0.0.1:5000'

// Функция для отправки запроса
async function sendGetRequest(url) {
  const response = await fetch(url, {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': "*",
    },
  })
  // Ошибка?
  if (!response.ok) {
    throw new Error(`Network response was not ok (Status: ${response.status}, ${response.statusText})`);
  }
  // Ошибки нет, передаём ответ сервера
  else {
    return response
  }
}
// http://127.0.0.1:5000/?email=email@.com&pass=password123

async function sendPostRequest(user: object) {
  // Отправляем запрос
  const response = await fetch(serverUrl, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': "*",
    },
    body: JSON.stringify(user)
  });
  // Ошибка?
  if (!response.ok) {
    throw new Error(`Network response was not ok (Status: ${response.status}, ${response.statusText})`);
  }
  // Ошибки нет, передаём ответ сервера
  else {
    return response
  }
}

// Функция для показывания результата регистрации на страницу
async function showRegisterStatus(response) {
  // Берём ответ сервера
  const data = await response.json();
  console.log('Response from server:', data);
  // Выводим нужный результат в зависимости от ответа сервера
  if (data == "True") {
    console.log("Пользователь успешно зарегестрирован.")
    WhichWarningIsVisibleRegister.value = true
  }
  else if (data == "False") {
    console.log("Данная почта уже зарегестрирована.")
    WhichWarningIsVisibleRegister.value = false
  }
}

async function showLoginStatus(response) {
  // Берём ответ сервера
  const data = await response.json();
  console.log('Response from server:', data);
  // Выводим нужный результат в зависимости от ответа сервера
  if (data == "True") {
    console.log("Пользователь успешно вошел в систему.")
    WhichWarningIsVisibleLogin.value = true
  }
  else if (data == "False") {
    console.log("Ошибка, проверьте данные ввода.")
    WhichWarningIsVisibleLogin.value = false
  }
}


// Функция которая создаёт пользователя
function createNewUser(name, email, pass) {
  let user = {
    username: name,
    email: email,
    pass: pass,
  }
  return user
}

function userLogin(email: string, pass: string) {
  let user = {
    email: email,
    pass: pass
  }
  return user
}

// Функция при клике
async function handleRegisterClick() {
  //  Создаём нового юзера
  let newUser = createNewUser(register_name.value, register_email.value, register_pass.value)
  console.log("input data:", newUser);

  // Проверка на пустые поля
  if (newUser.username == '' || newUser.email == '' || newUser.pass == '') {
    console.log("Одно или больше из полей пустое.")
    nullInputsRegister.value = true
    WhichWarningIsVisibleRegister.value = null
  }

  // Если все поля заполнены - идём дальше
  else {
    try {
      // Поля не пустые, все окей, меняем значение чтобы предупреждение пропало
      nullInputsRegister.value = false

      // Отправка запроса на сервер
      let serverResponse = await sendPostRequest(newUser)

      // Работаем с ответом сервера
      await showRegisterStatus(serverResponse)
    }

    // Ошибка?
    catch (error) {
      console.error('Error:', error);
    }
  }
};

async function handleLoginClick() {
  let existingUser = userLogin(login_email.value, login_pass.value)
  console.log(existingUser)


  if (existingUser.email == '' || existingUser.pass == '') {
    console.log("Одно или больше из полей пустое.")
    nullInputsLogin.value = true
    WhichWarningIsVisibleLogin.value = null
  }
  else {

    nullInputsRegister.value = false
    
  const queryString = new URLSearchParams(existingUser).toString();
  const urlWithParams = `${serverUrl}?${queryString}`;

  let serverResponse = await sendGetRequest(urlWithParams)
  console.log(serverResponse)

  await showLoginStatus(serverResponse)
  }
  // let data = await serverResponse.json()
  // console.log(data)
}

</script>

<template>
  <a href="https://front.codes/" class="logo" target="_blank">
    <img src="https://assets.codepen.io/1462889/fcy.png" alt="">
  </a>

  <div class="section">
    <div class="container">
      <div class="row full-height justify-content-center">
        <div class="col-12 text-center align-self-center py-5">
          <div class="section pb-5 pt-5 pt-sm-2 text-center">
            <h6 class="mb-0 pb-3"><span>Log In </span><span>Sign Up</span></h6>
            <input class="checkbox" type="checkbox" id="reg-log" name="reg-log" />
            <label for="reg-log"></label>
            <div class="card-3d-wrap mx-auto">
              <div class="card-3d-wrapper">
                <div class="card-front">
                  <div class="center-wrap">
                    <form action="">
                      <div class="section text-center">
                        <h4 class="mb-4 pb-3">Log In</h4>
                        <div class="form-group">
                          <input v-model="login_email" type="email" name="logemail" class="form-style login_email"
                            placeholder="Your Email" autocomplete="off">
                          <i class="input-icon uil uil-at"></i>
                        </div>
                        <div class="form-group mt-2">
                          <input v-model="login_pass" type="password" name="logpass" class="form-style login_pass"
                            placeholder="Your Password" autocomplete="off">
                          <i class="input-icon uil uil-lock-alt"></i>
                        </div>
                        <div class="register-failed-style" v-if="nullInputsLogin">
                          <p>Поля не должны быть пустыми.</p>
                        </div>
                        <div class="register-success-style" v-if="WhichWarningIsVisibleLogin == true"
                          :style="register_success">
                          <p>Вы вошли в систему.</p>
                        </div>
                        <div class="register-failed-style" v-else-if="WhichWarningIsVisibleLogin == false"
                          :style="register_failed">
                          <p>Ошибка, проверьте данные ввода.</p>
                        </div>
                        <a href="#" class="btn mt-4 login-submit" ref="login_submit" @click="handleLoginClick">submit</a>
                        <p class="mb-0 mt-4 text-center"><a href="#0" class="link">Forgot your password?</a></p>
                      </div>
                    </form>
                  </div>
                </div>
                <div class="card-back">
                  <div class="center-wrap">
                    <form action="">
                      <div class="section text-center">
                        <h4 class="mb-4 pb-3">Sign Up</h4>
                        <div class="form-group">
                          <input v-model="register_name" type="text" name="logname" class="form-style register-name"
                            placeholder="Your Full Name" autocomplete="off">
                          <i class="input-icon uil uil-user"></i>
                        </div>
                        <div class="form-group mt-2">
                          <input v-model="register_email" type="email" name="logemail" class="form-style register-email"
                            placeholder="Your Email" autocomplete="off">
                          <i class="input-icon uil uil-at"></i>
                        </div>
                        <div class="form-group mt-2">
                          <input v-model="register_pass" type="password" name="logpass" class="form-style register-pass"
                            placeholder="Your Password" autocomplete="off">
                          <i class="input-icon uil uil-lock-alt"></i>
                        </div>
                        <div class="register-failed-style" v-if="nullInputsRegister">
                          <p>Поля не должны быть пустыми.</p>
                        </div>
                        <div class="register-success-style" v-if="WhichWarningIsVisibleRegister == true"
                          :style="register_success">
                          <p>Регистрация пройдена успешно.</p>
                        </div>
                        <div class="register-failed-style" v-else-if="WhichWarningIsVisibleRegister == false"
                          :style="register_failed">
                          <p>Данная почта уже зарегестрирована.</p>
                        </div>
                        <a href="#" class="btn mt-4 register-submit" ref="register_submit"
                          @click="handleRegisterClick">submit</a>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css?family=Poppins:400,500,600,700,800,900');

.register-success-style {
  color: green;
}

.register-failed-style {
  color: red;
}

.invisible {
  display: none;
}

body {
  font-family: 'Poppins', sans-serif;
  font-weight: 300;
  font-size: 15px;
  line-height: 1.7;
  color: #c4c3ca;
  background-color: #1f2029;
  overflow-x: hidden;
}

a {
  cursor: pointer;
  transition: all 200ms linear;
}

a:hover {
  text-decoration: none;
}

.link {
  color: #c4c3ca;
}

.link:hover {
  color: #ffeba7;
}

p {
  font-weight: 500;
  font-size: 14px;
  line-height: 1.7;
}

h4 {
  font-weight: 600;
}

h6 span {
  padding: 0 20px;
  text-transform: uppercase;
  font-weight: 700;
}

.section {
  position: relative;
  width: 100%;
  display: block;
}

.full-height {
  min-height: 100vh;
}

[type="checkbox"]:checked,
[type="checkbox"]:not(:checked) {
  position: absolute;
  left: -9999px;
}

.checkbox:checked+label,
.checkbox:not(:checked)+label {
  position: relative;
  display: block;
  text-align: center;
  width: 60px;
  height: 16px;
  border-radius: 8px;
  padding: 0;
  margin: 10px auto;
  cursor: pointer;
  background-color: #ffeba7;
}

.checkbox:checked+label:before,
.checkbox:not(:checked)+label:before {
  position: absolute;
  display: block;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: #ffeba7;
  background-color: #102770;
  font-family: 'unicons';
  content: '\eb4f';
  z-index: 20;
  top: -10px;
  left: -10px;
  line-height: 36px;
  text-align: center;
  font-size: 24px;
  transition: all 0.5s ease;
}

.checkbox:checked+label:before {
  transform: translateX(44px) rotate(-270deg);
}


.card-3d-wrap {
  position: relative;
  width: 440px;
  max-width: 100%;
  height: 400px;
  -webkit-transform-style: preserve-3d;
  transform-style: preserve-3d;
  perspective: 800px;
  margin-top: 60px;
}

.card-3d-wrapper {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  -webkit-transform-style: preserve-3d;
  transform-style: preserve-3d;
  transition: all 600ms ease-out;
}

.card-front,
.card-back {
  width: 100%;
  height: 100%;
  background-color: #2a2b38;
  background-image: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/1462889/pat.svg');
  background-position: bottom center;
  background-repeat: no-repeat;
  background-size: 300%;
  position: absolute;
  border-radius: 6px;
  left: 0;
  top: 0;
  -webkit-transform-style: preserve-3d;
  transform-style: preserve-3d;
  -webkit-backface-visibility: hidden;
  -moz-backface-visibility: hidden;
  -o-backface-visibility: hidden;
  backface-visibility: hidden;
}

.card-back {
  transform: rotateY(180deg);
}

.checkbox:checked~.card-3d-wrap .card-3d-wrapper {
  transform: rotateY(180deg);
}

.center-wrap {
  position: absolute;
  width: 100%;
  padding: 0 35px;
  top: 50%;
  left: 0;
  transform: translate3d(0, -50%, 35px) perspective(100px);
  z-index: 20;
  display: block;
}


.form-group {
  position: relative;
  display: block;
  margin: 0;
  padding: 0;
}

.form-style {
  padding: 13px 20px;
  padding-left: 55px;
  height: 48px;
  width: 100%;
  font-weight: 500;
  border-radius: 4px;
  font-size: 14px;
  line-height: 22px;
  letter-spacing: 0.5px;
  outline: none;
  color: #c4c3ca;
  background-color: #1f2029;
  border: none;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
  box-shadow: 0 4px 8px 0 rgba(21, 21, 21, .2);
}

.form-style:focus,
.form-style:active {
  border: none;
  outline: none;
  box-shadow: 0 4px 8px 0 rgba(21, 21, 21, .2);
}

.input-icon {
  position: absolute;
  top: 0;
  left: 18px;
  height: 48px;
  font-size: 24px;
  line-height: 48px;
  text-align: left;
  color: #ffeba7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:-ms-input-placeholder {
  color: #c4c3ca;
  opacity: 0.7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input::-moz-placeholder {
  color: #c4c3ca;
  opacity: 0.7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:-moz-placeholder {
  color: #c4c3ca;
  opacity: 0.7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input::-webkit-input-placeholder {
  color: #c4c3ca;
  opacity: 0.7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:focus:-ms-input-placeholder {
  opacity: 0;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:focus::-moz-placeholder {
  opacity: 0;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:focus:-moz-placeholder {
  opacity: 0;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:focus::-webkit-input-placeholder {
  opacity: 0;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.btn {
  border-radius: 4px;
  height: 44px;
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
  padding: 0 30px;
  letter-spacing: 1px;
  display: -webkit-inline-flex;
  display: -ms-inline-flexbox;
  display: inline-flex;
  -webkit-align-items: center;
  -moz-align-items: center;
  -ms-align-items: center;
  align-items: center;
  -webkit-justify-content: center;
  -moz-justify-content: center;
  -ms-justify-content: center;
  justify-content: center;
  -ms-flex-pack: center;
  text-align: center;
  border: none;
  background-color: #ffeba7;
  color: #102770;
  box-shadow: 0 8px 24px 0 rgba(255, 235, 167, .2);
}

.btn:active,
.btn:focus {
  background-color: #102770;
  color: #ffeba7;
  box-shadow: 0 8px 24px 0 rgba(16, 39, 112, .2);
}

.btn:hover {
  background-color: #102770;
  color: #ffeba7;
  box-shadow: 0 8px 24px 0 rgba(16, 39, 112, .2);
}




.logo {
  position: absolute;
  top: 30px;
  right: 30px;
  display: block;
  z-index: 100;
  transition: all 250ms linear;
}

.logo img {
  height: 26px;
  width: auto;
  display: block;
}
</style>