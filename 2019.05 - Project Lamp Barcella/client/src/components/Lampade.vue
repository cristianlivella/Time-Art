<template>
    <div class="hello">
        <div class="container container-full">
            <div class='cose'>
                <div class="lamp" v-for="(lamp, index) in lamps" :key="lamp.id" v-bind:style="[lampCurrentColors[index]==0 ? {backgroundColor: '#f0f8ff'} : {backgroundColor: colors[lampCurrentColors[index]-1].hexValue}]"></div>
            </div>
        </div>
        <div class="container">
            <table class="table table-bordered">
                <tbody
                    <tr v-for="(lamp, index) in lamps" :key="lamp.id">
                        <td>Lampada {{ index+1 }}</td>
                        <td><span v-if="arduinoStatus[index]==0" style="color: #ff0000">OFFLINE</span> <span v-if="arduinoStatus[index]==1" style="color: #008000">ONLINE</span></td>
                        <td style="padding: 0px">
                            <button v-for="(color, colorIndex) in colors" v-on:click="changeColor(index+1, colorIndex+1)" type="button" class="btn btn-light" style="width: 35px; height: 35px; margin: 5px; border: 1px solid #ccc" v-bind:style="{ backgroundColor: color.hexValue}"> </button>
                        </td>
                        <td style="padding: 5px"><button v-on:click="changeColor(index+1, 0)" type="button" class="btn btn-light" style="border: 1px solid #ccc" >Spegni</button></td>
                    </tr>
                    <tr>
                        <td>Tutte le lampade</td>
                        <td></td>
                        <td style="padding: 0px">
                            <button v-for="(color, colorIndex) in colors" v-on:click="changeColor(0, colorIndex+1)" type="button" class="btn btn-light" style="width: 35px; height: 35px; margin: 5px; border: 1px solid #ccc" v-bind:style="{ backgroundColor: color.hexValue}"> </button>
                        </td>
                        <td style="padding: 5px"><button v-on:click="changeColor(0, 0)" type="button" class="btn btn-light" style="border: 1px solid #ccc" >Spegni</button></td>
                    </tr>
                </tbody>
            </table>
            <div class="container">
                <table class="table table-bordered">
                    <tbody>
                        <tr>
                            <td v-for="index in totalGame" style="padding: 5px"><button v-on:click="startGame(index)" v-bind:class="[index==currentGameId ? 'btn-primary' : 'btn-light']" type="button" class="btn" style="border: 1px solid #ccc" >Gioco {{ index }}</button></td>
                            <td style="width:300px; padding: 4px">
                                <div class="form-group row" style="margin-bottom: 0">
                                    <label for="example-number-input" class="col-5 col-form-label">Time delay</label>
                                    <div class="col-7">
                                        <input class="form-control" type="number" v-model.number="timeDelay" @change="updateTimeDelay" @input="updateTimeDelay" id="form-timeDelay">
                                    </div>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Lampade',
    data() {
        return {
            msg: 'Lampade',
            lamps: [],
            colors: [],
            arduinoStatus: [],
            lampCurrentColors: [],
            currentGameId: 0,
            totalGame: 0,
            timeDelay: 500,
        };
    },
    methods: {
        getLamps() {
            axios.get(`${this.$apiBaseUrl}/getLamps`)
            .then((res) => {
                this.lamps = res.data;
            });
        },
        getColors() {
            axios.get(`${this.$apiBaseUrl}/getColors`)
            .then((res) => {
                this.colors = res.data;
            });
        },
        changeColor(lampId, colorId) {
            axios.get(`${this.$apiBaseUrl}/changeColor/${lampId}/${colorId}`);
        },
        startGame(gameId) {
            axios.get(`${this.$apiBaseUrl}/startGame/${gameId}`);
        },
        updateTimeDelay() {
            axios.get(`${this.$apiBaseUrl}/setTime/${this.timeDelay}`);
        },
    },
    created() {
        this.getLamps();
        this.getColors();
    },
    sockets:{
        connect: function(data) {
            console.log("Socket connected")
        },
        projectlamp: function (data) {
            this.arduinoStatus = data.arduinoStatus;
            this.lampCurrentColors = data.lampCurrentColors;
            this.currentGameId = data.currentGameId;
            this.totalGame = data.totalGame;
            this.timeDelay = data.timeDelay;
            //console.log(this.lampCurrentColors);
        },
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-weight: normal;
}
.container-full {
    margin: 0 auto;
    width: 100%;
    max-width: 1920px;
}
.lamp {
    box-shadow: 2px 2px 2px grey;
    border: 1px solid grey;
    height: 180px;
    width: 180px;
    margin: 10px;
    display: inline-block;
}
</style>
