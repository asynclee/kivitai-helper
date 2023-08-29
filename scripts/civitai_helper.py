import modules.scripts as scripts
import gradio as gr
import os
from modules import script_callbacks
from scripts.ch_lib import model
from scripts.ch_lib import model_action_civitai
from scripts.ch_lib import setting
from scripts.ch_lib import util

# root path
root_path = os.getcwd()

# extension path
extension_path = scripts.basedir()

model.get_custom_model_folder()
setting.load()

# set proxy
if setting.data["general"]["proxy"]:
    util.printD("Set Proxy: "+setting.data["general"]["proxy"])
    util.proxies = {
        "http": setting.data["general"]["proxy"],
        "https": setting.data["general"]["proxy"],
    }


def on_ui_tabs():
    # ====Event's function====
    def get_model_info_by_url(url):
        r = model_action_civitai.get_model_info_by_url(url)

        model_info = {}
        model_name = ""
        model_type = ""
        subfolders = []
        version_strs = []
        if r:
            model_info, model_name, model_type, subfolders, version_strs = r

        return [model_info, model_name, model_type, dl_subfolder_drop.update(choices=subfolders), dl_version_drop.update(choices=version_strs)]

    # ====UI====
    with gr.Blocks(analytics_enabled=False) as civitai_helper:
        dl_model_info = gr.State({})

        with gr.Box(elem_classes="ch_box"):
            with gr.Column():
                gr.Markdown("### Download Model")
                with gr.Row():
                    dl_model_url_or_id_txtbox = gr.Textbox(label="Diffusion Art Hub URL", lines=1, value="")
                    dl_model_info_btn = gr.Button(value="1. Get Model Info by Diffusion Art Hub Url", variant="primary")

                gr.Markdown(value="2. Pick Subfolder and Model Version")
                with gr.Row():
                    dl_model_name_txtbox = gr.Textbox(label="Model Name", interactive=False, lines=1, value="")
                    dl_model_type_txtbox = gr.Textbox(label="Model Type", interactive=False, lines=1, value="")
                    dl_subfolder_drop = gr.Dropdown(choices=[], label="Sub-folder", value="", interactive=True, multiselect=False)
                    dl_version_drop = gr.Dropdown(choices=[], label="Model Version", value="", interactive=True, multiselect=False)
                    dl_all_ckb = gr.Checkbox(label="Download All files", value=False, elem_id="ch_dl_all_ckb", elem_classes="ch_vpadding")
                
                dl_civitai_model_by_id_btn = gr.Button(value="3. Download Model", variant="primary")
                dl_log_md = gr.Markdown(value="Check Console log for Downloading Status")

        # footer
        gr.Markdown(f"<center>version:{util.version}</center>")

        dl_model_info_btn.click(
            get_model_info_by_url,
            inputs=dl_model_url_or_id_txtbox,
            outputs=[dl_model_info, dl_model_name_txtbox, dl_model_type_txtbox, dl_subfolder_drop, dl_version_drop])
        dl_civitai_model_by_id_btn.click(
            model_action_civitai.dl_model_by_input,
            inputs=[dl_model_info, dl_model_type_txtbox, dl_subfolder_drop, dl_version_drop,
                    dl_all_ckb],
            outputs=dl_log_md)

    # the third parameter is the element id on html, with a "tab_" as prefix
    return (civitai_helper, "Model Downloader", "model_downloader"),


script_callbacks.on_ui_tabs(on_ui_tabs)
