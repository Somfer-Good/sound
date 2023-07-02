<template>
  <div class="old-film">
    <div class="film">
      <div class="effect">
        <div class="grain">
        </div>
      </div>
    </div>
  </div>
  <div style="height: 100vh;display: flex;flex-direction: column;box-sizing: border-box;padding: 5px">
    <div class="header-container">
      <h1 class="title">ЕЖК-7</h1>
      <span class="header-descr">БСВВ Настройщик. СССР. 1954</span>
    </div>
    <div class="flex-cont">
      <div class="left-container container">
        <button class="button-style noCursor">Расшифровка</button>
      </div>
      <div class="container">
        <div class="main" style="position: relative">
          <label for="fileInput" :class="isDragging && 'drag'"
                 class="dropzone-container"
                 @dragover="dragover"
                 @dragleave="dragleave"
                 @drop="drop"
          >
            <input
                type="file"
                name="file"
                id="fileInput"
                class="hidden-input"
                @change="onChange"
                ref="file"
                accept=".wav"

            />

            <div  class="file-label">
              <div v-if="isDragging">Отпустите файл.</div>
              <div v-else>Нажмите или перетащите файл.</div>
            </div>
          </label>
          <div class="preview-container mt-4" v-if="files.length">
            <div v-for="file in files" :key="file.name" class="preview-card">
              <div>
                <p class="nameFile">
                  {{ file.name }}
                </p>
              </div>
              <div>
                <button
                    class="ml-2"
                    type="button"
                    @click="remove(files.indexOf(file))"
                    title="Remove file"
                >
                  <b>×</b>
                </button>
              </div>
            </div>
          </div>
          <div class="preview-container mt-4" v-if="flag">
            <div class="preview-card">
              <div>
                <p class="nameFile">
                  Такой тип файла не поддерживается
                </p>
              </div>
              <div>
              </div>
            </div>
          </div>
        </div>
        <button class="button-style" v-on:click="send">Отправить</button>
      </div>
      <div class="container right-container">
        <div class="decodingMessage">{{text}}</div>
        <button class="button-style" style="margin-top: auto" @click="copy">Скопировать</button>
      </div>
    </div>
  </div>

</template>

<script>
import axios from "axios";
export default {
  name: 'App',
  data() {
    return {
      text: 'Отправьте файл,что бы получить текст!',
      isDragging: false,
      files: [],
      flag:false,

    }
  },
  methods: {
    copy(){
       navigator.clipboard.writeText(this.text)
    },
    onChange() {
      if(this.$refs.file.files.length &&this.$refs.file.files[0].type==='audio/wav'){
        this.flag = false
        this.files = [this.$refs.file.files[0]];
        return
      }
      this.flag = true
    },
    dragover(e) {
      e.preventDefault();
      this.isDragging = true;
    },
    dragleave() {
      this.isDragging = false;
    },
    drop(e) {
      e.preventDefault();
      this.$refs.file.files = e.dataTransfer.files;
      this.onChange();
      this.isDragging = false;
    },
    remove(i) {
      this.files.splice(i, 1);
    },
    send(){
      if (this.files.length!==0){
        let reader = new FileReader()
        reader.addEventListener('load',(res)=>{
          axios.post('http://127.0.0.1:5050/decrypt',{'wav':res.target.result.split("base64,")[1]}).then(data=>{this.text=data.data.text}).catch(()=>{this.text='Ошибка файла!'})
        })
        reader.readAsDataURL(this.files[0])
      }
    }
  }
}
</script>

<style>

@font-face {
  font-family: "atomic";
  src: url('./font/USSR_STENCIL.otf');
}

body {
  font-family: "atomic";
  background-color: black;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 15px 15px 0 0;
  border: 3px solid #96303c;
  padding: 15px;
}
.header-descr {
  color: gray;
}
.title {
  color: white;
  font-size: 25px;
}
.sub-title {
  color: white;
  font-size: 15px;
}
.left-container {
  margin-top: 10px;
  border-radius: 0 0 0 15px ;
  border: 3px solid #96303c;
}
.right-container {
  overflow-wrap: break-word;
  border-radius: 0 0 15px 0;
}
.button-style {
  font-family: "atomic";
  cursor: pointer;
  position: relative;
  display: flex;
  justify-content: center;
  width: 95%;
  margin: 10px auto;
  color: white;
  text-transform: uppercase;
  outline: none;
  border: none;
  padding: 15px;
  background-color: #A43838;
  font-size: 20px;
  letter-spacing: 3px;
  text-decoration: none;
}
.flex-cont {
  flex: 1;
  display: flex;
  gap: 10px;
}
#app{
  position: relative;

}
.flex-cont .container {
  display: flex;
  flex-direction: column;
  margin-top: 10px;
  min-height: 500px;
  flex: 1;
  border: 3px solid #96303c;
}

.old-film *,
.old-film *:before,
.old-film *:after {
  position: absolute;
}
.old-film {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  --filmbg: rgba(51,0,0,0.8);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  transition: all 0.5s ease 0s;
  border-radius: 15px;
}
.old-film:after {
  content: "";
  width: 100%;
  height: 100%;
  box-shadow: 0 0 180px 0 var(--filmbg) inset, 0 0 40px 5px var(--filmbg) inset, 0 0 10px 10px var(--filmbg);
  position: absolute;
}
.film,
.effect {
  width: 100%;
  height: 100%;
  filter: blur(0.45px) drop-shadow(0 0 0 red);
}
.film:after,
.effect:after {
  content: '';
  width: 120%;
  height: 100%;
  top: 0;
  left: 0;
  padding-left: 100px;
  opacity: 0.5;
  animation: film-scratch 0.45s steps(1) infinite;
  background: repeating-linear-gradient(90deg, #0002 0 2px, transparent 4px 37%);
}
.effect:after {
  left: 30%;
  animation: effect-scratch 2s infinite;
}
.grain {
  width: 100%;
  height: 100%;
}
.grain:after {
  content: '';
  width: 110%;
  height: 110%;
  top: -5%;
  left: -5%;
  opacity: .25;
  background-image: repeating-conic-gradient(var(--filmbg) 0%, transparent .00003%, transparent .0005%, transparent .00095%), repeating-conic-gradient(var(--filmbg) 0%, transparent .00005%, transparent 0.00015%, transparent 0.0009%);
  animation: grain 0.5s steps(1) infinite;
}

.decodingMessage{
  overflow-y: auto;
  max-height: 700px;
  max-width: 500px;
  color: white;
  font-family: "atomic",serif;
  padding: 10px;
  letter-spacing: 1px;
}
@keyframes grain {
  0%, 100% { transform: translate(0, 0); }
  10% { transform: translate(-1%, -1%); }
  20% { transform: translate(1%, 1%); }
  30% { transform: translate(-2%, -2%); }
  40% { transform: translate(3%, 3%); }
  50% { transform: translate(-3%, -3%); }
  60% { transform: translate(4%, 4%); }
  70% { transform: translate(-4%, -4%); }
  80% { transform: translate(2%, 2%); }
  90% { transform: translate(-3%, -3%); }
}
@keyframes film-scratch {
  0%, 100% { transform: translateX(0); opacity: 0.5; }
  10% { transform: translateX(-1%); }
  20% { transform: translateX(1%); }
  30% { transform: translateX(-2%); opacity: 0.75; }
  40% { transform: translateX(3%); }
  50% { transform: translateX(-3%); opacity: 0.5; }
  60% { transform: translateX(8%); }
  70% { transform: translateX(-3%); }
  80% { transform: translateX(10%); opacity: 0.25; }
  90% { transform: translateX(-2%); }
}
@keyframes effect-scratch {
  0% { transform: translateX(0); opacity: 0.75; }
  10% { transform: translateX(-1%); }
  20% { transform: translateX(1%); }
  30% { transform: translateX(-2%); }
  40% { transform: translateX(3%); }
  50% { transform: translateX(-3%); opacity: 0.5; }
  60% { transform: translateX(8%); }
  70% { transform: translateX(-3%); }
  80% { transform: translateX(10%); opacity: 0.25; }
  90% { transform: translateX(20%); }
  100% { transform: translateX(30%); }
}
.old-film.sepia {
  filter: sepia(0.75);
}
.old-film.invert .film {
  filter: invert(1)
}

html,#app {
  height: 100vh;
}
body {
  margin: 0;
  height: 100vh;
}
.form {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.nameFile {
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 450px;
}
.main {
  display: flex;
  flex-direction: column;
  flex: 1;
  align-items: center;
  justify-content: center;
  text-align: center;
  box-sizing: border-box;
  padding: 10px;
}

.dropzone-container {
  cursor: pointer;
  position: relative;
  z-index: 5;
  box-sizing: border-box;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
//border: 2px dashed red;
//background-color: transparent;
  color: lightgray;
}
.drag {
  border: 2px dashed red;
  background-color: transparent;
}

.hidden-input {
  opacity: 0;
  overflow: hidden;
  position: absolute;
  width: 1px;
  height: 1px;
}

.file-label {
  font-size: 20px;
  display: block;
  cursor: pointer;
}

.preview-container {
  position: relative;
  color: white;
  z-index: 7;
  display: flex;
  margin-top: 2rem;
}

.preview-card {
  display: flex;
  border: 1px solid #a2a2a2;
  padding: 5px;
  margin-left: 5px;
}

.preview-img {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  border: 1px solid #a2a2a2;
  background-color: #a2a2a2;
}

.noCursor{
  cursor: default !important;
}
</style>
