import gradio as gr
from everything_search import EverythingSearch

es = EverythingSearch()

def search_files(query, max_results, regex, case_sensitive, files_only, folders_only):
    return es.search(
        query,
        max_results=int(max_results),
        regex=regex,
        case_sensitive=case_sensitive,
        files_only=files_only,
        folders_only=folders_only,
    )

def search_by_extension(extension, max_results):
    return es.search_by_extension(extension, max_results=int(max_results))

def search_by_size(size_filter, max_results):
    return es.search_by_size(size_filter, max_results=int(max_results))

def search_recent(days, max_results):
    return es.search_recent(int(days), max_results=int(max_results))

with gr.Blocks() as demo:
    gr.Markdown("# Everything Search Gradio Interface")

    with gr.Tab("Advanced Search"):
        with gr.Row():
            query_input = gr.Textbox(label="Query")
            max_results_input = gr.Number(label="Max Results", value=10)
        with gr.Row():
            regex_checkbox = gr.Checkbox(label="Regex")
            case_sensitive_checkbox = gr.Checkbox(label="Case Sensitive")
            files_only_checkbox = gr.Checkbox(label="Files Only", value=True)
            folders_only_checkbox = gr.Checkbox(label="Folders Only")
        search_button = gr.Button("Search")
        search_output = gr.JSON()
        search_button.click(
            search_files,
            inputs=[
                query_input,
                max_results_input,
                regex_checkbox,
                case_sensitive_checkbox,
                files_only_checkbox,
                folders_only_checkbox,
            ],
            outputs=search_output,
        )

    with gr.Tab("Search by Extension"):
        ext_input = gr.Textbox(label="Extension (e.g., 'py', 'txt')")
        ext_max_results_input = gr.Number(label="Max Results", value=10)
        ext_search_button = gr.Button("Search")
        ext_search_output = gr.JSON()
        ext_search_button.click(
            search_by_extension,
            inputs=[ext_input, ext_max_results_input],
            outputs=ext_search_output,
        )

    with gr.Tab("Search by Size"):
        size_input = gr.Textbox(label="Size Filter (e.g., '>100MB', '<1KB')")
        size_max_results_input = gr.Number(label="Max Results", value=10)
        size_search_button = gr.Button("Search")
        size_search_output = gr.JSON()
        size_search_button.click(
            search_by_size,
            inputs=[size_input, size_max_results_input],
            outputs=size_search_output,
        )

    with gr.Tab("Search Recent Files"):
        days_input = gr.Number(label="Days", value=7)
        recent_max_results_input = gr.Number(label="Max Results", value=10)
        recent_search_button = gr.Button("Search")
        recent_search_output = gr.JSON()
        recent_search_button.click(
            search_recent,
            inputs=[days_input, recent_max_results_input],
            outputs=recent_search_output,
        )

if __name__ == "__main__":
    demo.launch()
