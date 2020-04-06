<template>
    <div class="hello">
        <div class="container">
            <h2>Utenti autorizzati</h2>
        </div>
        <div class="container">
            <table class="table table-bordered">
                <tbody>
                    <tr>
                        <th>Nome</th>
                        <th>Chat ID</th>
                        <th>Scadenza</th>
                        <th>Azioni</th>
                    </tr>
                    <tr v-for="(user, index) in authorizedUsers" :key="user.id">
                        <td>{{ user.name }}</td>
                        <td>{{ user.chatId }}</td>
                        <td>{{ user.expire | formatDate }}</td>
                        <td style="padding: 5px">
                            <button v-if="user.expire!=0" v-on:click="add10minutes(user.id)" type="button" class="btn btn-primary" style="border: 1px solid #ccc" >Aggiungi 10 minuti</button>
                            <button v-on:click="removeUser(user.id)" type="button" class="btn btn-danger" style="border: 1px solid #ccc" >Rimuovi</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <hr>
        <div class="container">
            <h2>Richieste autorizzazione</h2>
        </div>
        <div class="container">
            <table class="table table-bordered">
                <tbody>
                    <tr>
                        <th>Nome</th>
                        <th>Chat ID</th>
                        <th>Azioni</th>
                    </tr>
                    <tr v-for="(request, index) in usersRequests" :key="request.id">
                        <td>{{ request.name }}</td>
                        <td>{{ request.chatId }}</td>
                        <td style="padding: 5px">
                            <button v-on:click="giveAuth(request.id, 0)" type="button" class="btn btn-primary" style="border: 1px solid #ccc" >Autorizzazione temporanea</button>
                            <button v-on:click="giveAuth(request.id, 1)" type="button" class="btn btn-primary" style="border: 1px solid #ccc" >Autorizzazione permanente</button>
                            <button v-on:click="rejectRequest(request.id)" type="button" class="btn btn-danger" style="border: 1px solid #ccc" >Rifiuta</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Telegram',
    data() {
        return {
            msg: 'Telegram',
            authorizedUsers: [],
            usersRequests: [],
            timer1: '',
            timer2: '',
        };
    },
    methods: {
        getAuthorizedUsers() {
            axios.get(`${this.$apiBaseUrl}/telegramBot/getAuthorizedUsers`)
            .then((res) => {
                this.authorizedUsers = res.data;
            });
        },
        getUsersRequets() {
            axios.get(`${this.$apiBaseUrl}/telegramBot/getUsersRequests`)
            .then((res) => {
                this.usersRequests = res.data;
            });
        },
        add10minutes(userId) {
            axios.get(`${this.$apiBaseUrl}/telegramBot/add10minutes/${userId}`);
            this.getAuthorizedUsers();
            this.getUsersRequets();
        },
        removeUser(userId) {
            axios.get(`${this.$apiBaseUrl}/telegramBot/removeUser/${userId}`);
            this.getAuthorizedUsers();
            this.getUsersRequets();
        },
        giveAuth(requestId, permanent) {
            axios.get(`${this.$apiBaseUrl}/telegramBot/giveAuth/${requestId}/${permanent}`);
            this.getAuthorizedUsers();
            this.getUsersRequets();
        },
        rejectRequest(requestId) {
            axios.get(`${this.$apiBaseUrl}/telegramBot/rejectRequest/${requestId}`);
            this.getAuthorizedUsers();
            this.getUsersRequets();
        },
        cancelAutoUpdate: function() {
            clearInterval(this.timer)
        },
    },
    created() {
        this.getAuthorizedUsers();
        this.getUsersRequets();
        this.timer1 = setInterval(this.getAuthorizedUsers, 10000);
        this.timer2 = setInterval(this.getUsersRequets, 10000);
    },
    beforeDestroy() {
        clearInterval(this.timer1)
        clearInterval(this.timer2)
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-weight: normal;
}
</style>
