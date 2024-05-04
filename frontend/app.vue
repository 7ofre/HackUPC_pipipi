<!-- app.vue -->
<template>
    <div>
        <h1>Enter Your Input</h1>
        <input type="text" v-model="travellerName" placeholder="Enter your input" required>
        <button @click="findCompanions">Submit</button>
        <div v-if="companions.length > 0">
            <h2>Potential Companions:</h2>
            <ul>
                <li v-for="companion in companions" :key="companion.travellerName">
                    {{ companion.travellerName }} - {{ companion.departureDate }} to {{ companion.returnDate }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            travellerName: '',
            companions: []
        };
    },
    methods: {
        async findCompanions() {
            const response = await fetch('/find-companions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    travellerName: this.travellerName
                })
            });
            this.companions = await response.json();
        }
    }
};
</script>

<style scoped>
/* Add your CSS styles here */
</style>
