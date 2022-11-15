# Write Final Documents
file.copy(
    paste('_docs', label_name, label_run, 'summary.md', sep = '//')
    , paste(label_name, '_Results.md', sep = '')
    , overwrite = TRUE
    )
render(
    input = paste(label_name, '_Results.md', sep = '')
    , output_format = 'html_document'
    , output_file = paste(label_home, '//', label_user, '//', label_character, '//', label_project, '//', label_name, '_Results.html', sep = '')
    )
render(
    input = paste(label_name, '_Results.md', sep = '')
    , output_format = 'word_document'
    ,  output_file = paste(label_home, '//', label_user, '//', label_character, '//', label_project, '//', label_name, '_Results.docx', sep = '')
    )