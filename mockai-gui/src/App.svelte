<script>
  import ResponseForm from "./lib/ResponseForm.svelte";
  import { onMount } from "svelte";

  let responses;

  async function get_responses() {
    let res = await fetch("http://localhost:8100/api/responses/get");
    return await res.json();
  }

  onMount(async () => {
    responses = await get_responses();
  });
</script>

<main class="min-h-screen bg-gray-100 py-8">
  <h1 class="text-3xl font-bold text-gray-800 mb-8 ml-8">MockAI Responses</h1>
  {#if responses}
    {#each responses as response, i}
      <ResponseForm
        number={i + 1}
        select_choice={response.type}
        input={response.input}
        output={response.output}
      />
    {/each}
  {:else}
    <p class="text-center text-gray-600">Loading responses...</p>
  {/if}
</main>

<style>
</style>
