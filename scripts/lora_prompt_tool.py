import modules.scripts as scripts
import gradio as gr
import modules
from modules import script_callbacks
from modules import shared
from modules.ui_components import ToolButton
from modules.ui import create_refresh_button
from scripts.loraprompt_lib import libdata
from scripts.loraprompt_lib import model
from scripts.loraprompt_lib import ajax_action
from scripts.loraprompt_lib import dataframe_edit
from modules import localization
from scripts.loraprompt_lib import util
from scripts.loraprompt_lib import setting

model.get_custom_model_folder()
setting.load_setting()
util.set_debug_logging_state(ajax_action.flag_to_boolean(setting.get_setting("debug")))

def on_ui_tabs():
    #local_code = getattr(shared.opts, "localization", "en")
    #if getattr(shared.opts, "bilingual_localization_enabled", False) and (local_code == "en" or str(local_code).lower() == "none"):
        #local_code = getattr(shared.opts, "bilingual_localization_file", local_code)
    #localization.load_localization(local_code)
    with gr.Blocks(analytics_enabled=False) as lora_prompt_helper:
        txt2img_prompt = modules.ui.txt2img_paste_fields[0][0]
        txt2img_neg_prompt = modules.ui.txt2img_paste_fields[1][0]
        img2img_prompt = modules.ui.img2img_paste_fields[0][0]
        img2img_neg_prompt = modules.ui.img2img_paste_fields[1][0]
        with gr.Tab('Edit Model Trigger Words'):
            with gr.Box(elem_classes="lorahelp_box"):
                #模型基礎資料區
                with gr.Column():
                    gr.Markdown(f"### {'Edit Model Basic Data'}")
                    with gr.Row():
                        with gr.Column():
                            js_model_type = gr.Textbox(label="Model type", interactive=False)
                            js_subtype = gr.Textbox(label="Type", interactive=True, placeholder="EX: LoCon")
                            js_model_name = gr.Textbox(label="Name", interactive=True)
                            js_model_path = gr.Textbox(label="Model Path", interactive=False)
                        gr.HTML(f"<div id=\"lorahelp_js_image_area\">{'You DID NOT load any model!'}</div>")
                    with gr.Row():
                        js_suggested_weight = gr.Textbox(label="Suggested weight", interactive=True, placeholder="EX: 1.0")
                        js_model_params = gr.Textbox(label="Model params", interactive=True, placeholder="EX: 0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
            with gr.Box(elem_classes="lorahelp_box"):
                #提詞編輯區
                with gr.Column():
                    gr.Markdown(f"### {'Edit Model Trigger Words'}")
                    with gr.Tab('Easy editing'):
                        with gr.Column(elem_id="lorahelp_simpleedit_group_main"):
                            simpleedit_main_name = gr.Textbox(label="name", interactive=True, placeholder="EX: draw a Mahiro")
                            simpleedit_main_triggerword = gr.Textbox(label="Trigger Word", interactive=True, placeholder="EX: mahiro_\\(onimai\\")
                        with gr.Column(elem_id="lorahelp_simpleedit_supergroup_other"):
                            with gr.Column(elem_id="lorahelp_simpleedit_group_extra"):
                                simpleedit_extra_enable = gr.Checkbox(value=False,label="Additional description", interactive=True, elem_id="lorahelp_simpleedit_group_extra_enabled")
                                with gr.Column(elem_id="lorahelp_simpleedit_group_extra_body"):
                                    simpleedit_extra_name = gr.Textbox(label="Additional description name", interactive=True, placeholder="EX: Characteristics of Mahiro")
                                    simpleedit_extra_triggerword = gr.Textbox(label="Description prompt", interactive=True, placeholder="EX: long_hair, brown_eyes")
                            with gr.Column(elem_id="lorahelp_simpleedit_group_neg"):
                                simpleedit_neg_enable = gr.Checkbox(value=False,label="Dedicated negative prompt", interactive=True, elem_id="lorahelp_simpleedit_group_neg_enabled")
                                with gr.Column(elem_id="lorahelp_simpleedit_group_neg_body"):
                                    simpleedit_neg_name = gr.Textbox(label="Dedicated negative prompt name", interactive=True, placeholder="EX: negative prompt for Mahiro")
                                    simpleedit_neg_triggerword = gr.Textbox(label="Negative prompt", interactive=True, placeholder="EX: ugly, bad")
                        simpleedit_apply = gr.Button(value="Apply data")
                        simpleedit_parms=[simpleedit_main_name, simpleedit_main_triggerword, simpleedit_extra_enable, simpleedit_extra_name, simpleedit_extra_triggerword, simpleedit_neg_enable, simpleedit_neg_name, simpleedit_neg_triggerword]

                    with gr.Tab('Advanced editing',elem_id="js_tab_adv_edit"):
                        js_dataedit_select_index = gr.Textbox(label="Select Index", visible=False, lines=1, value="", elem_id="lorahelp_dataedit_select_index_txtbox")
                        js_copy_paste_box = gr.Textbox(label="Copy paste", visible=False, lines=1, value="", elem_id="lorahelp_copy_paste_txtbox")
                        dataedit_add_event = gr.Button(value=libdata.add_symbol, visible=False, elem_id="lorahelp_dataedit_add_event")
                        dataedit_delete_event = gr.Button(value=libdata.delete_symbol, visible=False, elem_id="lorahelp_dataedit_delete_event")
                        dataedit_up_event = gr.Button(value=libdata.up_symbol, visible=False, elem_id="lorahelp_dataedit_up_event")
                        dataedit_down_event = gr.Button(value=libdata.down_symbol, visible=False, elem_id="lorahelp_dataedit_down_event")
                        dataedit_paste_event = gr.Button(value=libdata.paste_symbol, visible=False, elem_id="lorahelp_dataedit_paste_event")
                        dataedit_paste_append_event = gr.Button(value=libdata.paste_append_symbol, visible=False, elem_id="lorahelp_dataedit_paste_append_event")

                        #編輯工具列
                        with gr.Row():
                            ToolButton(value=libdata.add_symbol, elem_id="lorahelp_dataedit_add_btn")
                            ToolButton(value=libdata.delete_symbol, elem_id="lorahelp_dataedit_delete_btn")
                            ToolButton(value=libdata.up_symbol, elem_id="lorahelp_dataedit_up_btn")
                            ToolButton(value=libdata.down_symbol, elem_id="lorahelp_dataedit_down_btn")
                            ToolButton(value=libdata.copy_symbol, elem_id="lorahelp_dataedit_copy_btn")
                            ToolButton(value=libdata.paste_symbol, elem_id="lorahelp_dataedit_paste_btn")
                            ToolButton(value=libdata.paste_append_symbol, elem_id="lorahelp_dataedit_paste_append_btn")
                            ToolButton(value="", elem_id="lorahelp_oyama_mahiro")
                            dataedit_refresh_event = ToolButton(value=libdata.refresh_symbol, elem_id="lorahelp_dataedit_refresh_event_btn")
                            gr.Button(value="Translate prompt words into:", elem_id="lorahelp_dataedit_translate_btn")
                        gr.HTML(f"<div id=\"lorahelp_translate_area\"></div>")

                        #編輯區: 資料表
                        js_dataedit = gr.Dataframe(headers=[
                                "name", 
                                "Enter your prompt word (trigger word/prompt/negative prompt)", 
                                "Categorys of prompt", 
                                "Negative prompt: please enter Y if this prompt is a negative prompt."
                            ], datatype=["str", "str", "str", "str"], col_count=(4, "fixed"), elem_id="lorahelp_js_trigger_words_dataframe", interactive=True)
                        
                        #操作區
                        with gr.Row():
                            js_remove_duplicate_prompt_btn = gr.Button(value="Remove duplicate prompts")
                            js_remove_empty_prompt_btn = gr.Button(value="Remove empty prompts")
                        with gr.Column():
                            with gr.Row():
                                js_dataframe_filter = gr.Textbox(label="Search...", interactive=True, elem_id="lorahelp_js_dataframe_filter")
                            gr.Checkbox(value=False,label="Sorting", interactive=True, elem_id="lorahelp_sorting_group_enabled")
                        with gr.Column(elem_id="lorahelp_sorting_group"):
                            #排序功能
                            with gr.Row():
                                js_sort_order = gr.Radio(
                                    choices=[e.value for e in libdata.SortOrder], interactive=True, 
                                    label='Sort Order',
                                    elem_id="lorahelp_js_sort_order_radio"
                                )
                                js_sort_by_title_btn = gr.Button(value="Sort by title")
                                js_sort_by_prompt_btn = gr.Button(value="Sort by prompt")
                    with gr.Tab('JSON'):
                        with gr.Column():
                            with gr.Row():
                                json_refresh_event = ToolButton(value=libdata.refresh_symbol, elem_id="lorahelp_json_refresh_event_btn")
                            js_json_preview = gr.JSON()
            #輸出訊息框
            with gr.Box(elem_classes="lorahelp_box"):
                with gr.Column():
                    js_message_report = gr.Textbox(label="Message", interactive=False, elem_id="lorahelp_js_output_message")
            js_save_model_setting_btn = gr.Button(value="Save", 
                elem_id="lorahelp_js_save_model_setting_btn", variant="primary"
            )

            #導入功能區
            with gr.Box(elem_classes="lorahelp_box"):
                with gr.Column():
                    gr.Markdown(f"### {'Batch import prompts'}")
                    with gr.Row():
                        with gr.Column():
                            js_load_textbox_prompt_btn = gr.Button(value="Read prompts from text boxes", elem_id="lorahelp_js_load_textbox_prompt_btn")
                            js_load_civitai_setting_btn = gr.Button(value="Download configuration files from CivitAI", 
                                elem_id="lorahelp_js_load_civitai_setting_btn")
                            with gr.Row():
                                js_db_model_name = gr.Dropdown(
                                    label="Model", choices=sorted(model.get_db_models()), interactive=True
                                )
                                create_refresh_button(
                                    js_db_model_name,
                                    model.get_db_models,
                                    lambda: {"choices": sorted(model.get_db_models())},
                                    "lorahelp_refresh_db_models",
                                )
                            js_load_dreambooth_setting_btn = gr.Button(value="Load trigger words from Dreambooth model", 
                                elem_id="lorahelp_js_load_dreambooth_setting_btn")
                        text_import_txtbox = gr.Textbox(label="Enter prompts (one line for one trigger words)", lines=10, value="", 
                            elem_id="lorahelp_text_import_txtbox")

            json_ajax_txtbox = gr.Textbox(label="Model JSON", visible=False, lines=1, value="", elem_id="lorahelp_model_json_txtbox")
        with gr.Tab('Settings'):
            with gr.Box(elem_classes="lorahelp_box"):
                with gr.Column():
                    gr.Markdown(f"### {'Settings'}")
                    with gr.Row():
                        js_debug_logging = gr.Checkbox(label="Show debug message", value=ajax_action.flag_to_boolean(setting.get_setting("debug")), elem_id="lorahelp_js_debug_logging")
                        js_touch_mode = gr.Checkbox(label="Force touch mode", value=ajax_action.flag_to_boolean(setting.get_setting("touch_mode")), elem_id="lorahelp_js_touch_mode")
                    js_save_ext_setting_btn = gr.Button(value="Save Setting", 
                        elem_id="lorahelp_js_save_ext_setting_btn", variant="primary"
                    )
                    js_save_ext_setting_btn.click(setting.save_setting)
                    
        try:
            js_dataedit.select(dataframe_edit.get_select_index, outputs=[js_dataedit_select_index])
        except:
            gr.Textbox(label="select not support", lines=1, visible=False, value="", elem_id="lorahelp_select_not_support")
        from scripts.loraprompt_lib import extension_data
        gr.Textbox(label="extension name", lines=1, visible=False, value=extension_data.extension_name, elem_id="lorahelp_extension_name")

        js_debug_logging.change(util.set_debug_logging_state, inputs=[js_debug_logging]) 
        js_touch_mode.change(setting.set_touch_mode, inputs=[js_touch_mode]) 

        model_data_ui_input = [js_subtype, js_model_name, js_model_path, js_suggested_weight, js_model_params]

        #工具列事件
        dataedit_add_event.click(dataframe_edit.add_row, inputs=[js_dataedit_select_index, js_dataedit], outputs=[js_dataedit])
        dataedit_delete_event.click(dataframe_edit.delete_row, inputs=[js_dataedit_select_index, js_dataedit], outputs=[js_dataedit])
        dataedit_up_event.click(dataframe_edit.up_row, inputs=[js_dataedit_select_index, js_dataedit], outputs=[js_dataedit])
        dataedit_down_event.click(dataframe_edit.down_row, inputs=[js_dataedit_select_index, js_dataedit], outputs=[js_dataedit])
        dataedit_paste_event.click(dataframe_edit.paste_cell, inputs=[js_dataedit_select_index, js_copy_paste_box, js_dataedit], outputs=[js_dataedit])
        dataedit_paste_append_event.click(dataframe_edit.paste_merge_cell, inputs=[js_dataedit_select_index, js_copy_paste_box, js_dataedit], outputs=[js_dataedit])

        simpleedit_apply.click(dataframe_edit.save_to_dataframe, inputs=[js_dataedit, *simpleedit_parms], outputs=[js_dataedit])

        dataedit_refresh_event.click(ajax_action.reload_trigger_words, inputs=[js_model_type, js_model_path], 
            outputs=[js_model_type, *model_data_ui_input, js_dataedit, *simpleedit_parms, json_ajax_txtbox, js_json_preview])
        json_refresh_event.click(ajax_action.update_trigger_words_json, inputs=[*model_data_ui_input, js_dataedit, *simpleedit_parms, json_ajax_txtbox], 
            outputs=[js_json_preview])


        js_save_model_setting_btn.click(ajax_action.save_trigger_words, 
            inputs=[js_model_type, *model_data_ui_input, js_dataedit, *simpleedit_parms, json_ajax_txtbox], 
            outputs=[js_message_report]
        )
        js_load_civitai_setting_btn.click(ajax_action.get_setting_from_Civitai, 
            inputs=[js_model_type, *model_data_ui_input, js_dataedit, *simpleedit_parms, json_ajax_txtbox], 
            outputs=[js_message_report, js_model_type, *model_data_ui_input, js_dataedit, *simpleedit_parms, json_ajax_txtbox, js_json_preview]
        )
        js_load_dreambooth_setting_btn.click(ajax_action.get_setting_from_dreambooth, 
            inputs=[js_db_model_name, js_dataedit], 
            outputs=[js_message_report, js_dataedit]
        )
        js_load_textbox_prompt_btn.click(dataframe_edit.load_prompt_from_textbox, 
            inputs=[text_import_txtbox, js_dataedit], 
            outputs=[js_dataedit]
        )

        js_remove_duplicate_prompt_btn.click(dataframe_edit.remove_duplicate_prompt, 
            inputs=[js_dataedit], 
            outputs=[js_dataedit]
        )
        js_remove_empty_prompt_btn.click(dataframe_edit.remove_empty_prompt, 
            inputs=[js_dataedit], 
            outputs=[js_dataedit]
        )
        js_sort_by_title_btn.click(dataframe_edit.sort_by_title, 
            inputs=[js_sort_order, js_dataedit], 
            outputs=[js_dataedit]
        )
        js_sort_by_prompt_btn.click(dataframe_edit.sort_by_prompt, 
            inputs=[js_sort_order, js_dataedit], 
            outputs=[js_dataedit]
        )

        #, visible=False,
        js_ajax_txtbox = gr.Textbox(label="Request Msg From Js", visible=False, lines=1, value="", elem_id="lorahelp_js_ajax_txtbox")
        py_ajax_txtbox = gr.Textbox(label="Response Msg From Python", visible=False, lines=1, value="", elem_id="lorahelp_py_ajax_txtbox")

        js_cors_request_btn = gr.Button(value="CORS request", visible=False, elem_id="lorahelp_js_cors_request_btn")
        js_cors_request_btn.click(ajax_action.cors_request, inputs=[js_ajax_txtbox], outputs=[js_ajax_txtbox])

        js_update_trigger_words_btn = gr.Button(value="Update Trigger Words", visible=False, elem_id="lorahelp_js_update_trigger_words_btn")
        js_update_trigger_words_btn.click(ajax_action.update_trigger_words, 
            inputs=[js_ajax_txtbox], 
            outputs=[js_model_type, *model_data_ui_input, js_dataedit, *simpleedit_parms, json_ajax_txtbox, js_json_preview]
        )

        js_show_trigger_words_btn = gr.Button(value="Show Trigger Words", visible=False, elem_id="lorahelp_js_show_trigger_words_btn")
        js_show_trigger_words_btn.click(ajax_action.show_trigger_words, inputs=[js_ajax_txtbox], outputs=[js_ajax_txtbox])

        js_add_selected_trigger_word_btn = gr.Button(value="Add Selected Trigger Words", visible=False, elem_id="lorahelp_js_add_selected_trigger_word_btn")
        js_add_selected_trigger_word_btn.click(ajax_action.add_selected_trigger_word, inputs=[js_ajax_txtbox], outputs=[txt2img_prompt, img2img_prompt])

        js_add_selected_neg_trigger_word_btn = gr.Button(value="Add Selected Neg Trigger Words", visible=False, elem_id="lorahelp_js_add_selected_neg_trigger_word_btn")
        js_add_selected_neg_trigger_word_btn.click(ajax_action.add_selected_trigger_word, inputs=[js_ajax_txtbox], outputs=[txt2img_neg_prompt, img2img_neg_prompt])

    from scripts.loraprompt_lib import extension_data
    # the third parameter is the element id on html, with a "tab_" as prefix
    return (lora_prompt_helper , extension_data.extension_name_display, extension_data.extension_id),

script_callbacks.on_ui_tabs(on_ui_tabs)
