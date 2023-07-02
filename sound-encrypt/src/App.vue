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
        <button class="button-style">Шифровка</button>
      </div>
      <div class="container">
        <textarea  class="input_message" v-model="text" placeholder="Введи секретное сообщение"/>

        <div class="preview-container mt-4" v-if="flag">
          <div class="preview-card">
            <div>
              <p class="nameFile">
                Ошибка шифровки, возможно есть необрабатываемые символы!
              </p>
            </div>
            <div>
            </div>
          </div>
        </div>
        <button v-on:click="send" class="button-style" type="button" style="margin-top: auto">Зашифровать</button>
      </div>
      <div class="container" style="justify-content: space-between">
        <AVBars caps-color="red" bar-color="red" :src="src">
        </AVBars>
        <a ref="donAudio" class="button-style" download style="box-sizing: border-box">Скачать</a>
      </div>
    </div>
  </div>
</template>

<script>

import axios from "axios";
import {AVBars} from "vue-audio-visual";

export default {
  name: 'App',
  data() {
    return {
      text: '',
      urlD:'',
      src:'',
      flag:false,
      res:'res'
    }
  },
  components:{
    AVBars,
  },
  methods: {
      async send() {
        if (this.text !== '') {
          let Data={
            text:this.text
          }
          await axios.post('http://127.0.0.1:5000/encrypt', Data).then(data => {
            this.flag=false
            this.src="data:audio/wav;base64, "+data.data
            this.$refs.donAudio.href="data:audio/wav;base64, "+data.data
          }).catch(()=>{
            this.flag=true})
        }
      }
  },
  mounted() {
    document.querySelector(".container > audio").onended=()=>{
      document.querySelector('canvas').style.display='none';
    }
    document.querySelector(".container > audio").onplay=()=>{
      document.querySelector('canvas').style.display='block';
    }
  }
}
</script>

<style>
canvas {
  width: 95%;
  margin: 0 auto;
  margin-top: auto;
}
audio {
  width: 95%;
  margin: 0 auto;
  margin-top: 20px;
}
html,#app {
  height: 100vh;
}
body {
  margin: 0;
  height: 100vh;
}
@font-face {
  font-family: "USSR_STENCIL";
  src: url('font/USSR_STENCIL.otf');
}

body {
  font-family: 'USSR_STENCIL';
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
  font-family: "USSR_STENCIL";
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
.button-style, .nameFile  {
  font-family: "USSR_STENCIL";
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
  display: flex;
  gap: 10px;
  flex: 1;
}
#app{
  position: relative;
}
.input_message{
  font-family: "USSR_STENCIL";
  flex: 1;
  position: relative;
  resize: vertical;
  width: 95%;
  resize: none;
  margin: 10px auto;
  padding: 0;
  box-sizing: border-box;
  padding: 10px;
  color: white;
  background-color: transparent;
  min-height: 500px;
  display: flex;
  border-color: gray;
  margin: 10px auto;
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
.preview-container {
  position: relative;
  width: 95%;
  color: white;
  z-index: 7;
  display: flex;
  margin: 0 auto;
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.preview-card {
  display: flex;
  border: 1px solid #a2a2a2;
  padding: 5px;
  margin-left: 5px;
}

.nameFile{
  cursor: default !important;
}
</style>
