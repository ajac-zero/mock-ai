<script>
  import ResponseForm from "./lib/ResponseForm.svelte";
  import { onMount } from "svelte";

  let responses;

  async function get_responses() {
    let res = await fetch("http://localhost:8100/api/responses/read");
    return await res.json();
  }

  async function add_response() {
    await fetch("http://localhost:8100/api/responses/create");
    window.location.reload();
  }

  onMount(async () => {
    responses = await get_responses();
  });
</script>

<main class="min-h-screen bg-gray-100 py-8">
  <div class="mx-auto max-w-4xl p-4">
    <!-- Heading -->
    <h1 class="text-3xl font-bold text-gray-800 mb-8">MockAI Responses</h1>

    <!-- Responses List -->
    {#if responses}
      <div class="space-y-6">
        {#each responses as response, i}
          <ResponseForm
            number={i + 1}
            select_choice={response.type}
            input={response.input}
            output={response.output}
          />
        {/each}
      </div>
    {:else}
      <p class="text-center text-gray-600">Loading responses...</p>
    {/if}

    <!-- Add New Response Button -->
    <div class="mt-8 text-center">
      <button
        class="bg-blue-500 text-white px-6 py-3 rounded-md shadow hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
        onclick={add_response}
      >
        Add New Response
      </button>
    </div>
  </div>
</main>

<style>
</style>
