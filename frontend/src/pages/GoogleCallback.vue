<template>
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
        <div>
            <h2 style="text-align: center;">
                Authenticating via Google credentials...
            </h2>
            <div style="display: flex; justify-content: center;">
                <the-spinner></the-spinner>
            </div>
        </div>
    </div>
</template>


  
  
<script setup>
import TheSpinner from "@/components/layout/TheSpinner.vue";

import { onMounted } from 'vue';
import { useAuthStore } from "@/store/authStore";


const authStore = useAuthStore();


const authenticateViaBackend = async () => {
    const accessToken = new URLSearchParams(window.location.hash.substring(1)).get('access_token');
    const authenticationSuccess = await authStore.loginWithGoogle(accessToken);

    if (authenticationSuccess) {
        // Close the pop-up
        window.close();

        // Make sure the original tab is in full-screen mode
        // Redirect to main page
        if (window.opener) {
            window.opener.location.href = '/';

        }
    }
};

onMounted(async () => {
    await authenticateViaBackend();
})

</script>
  
  
  