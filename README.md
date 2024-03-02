# admission_documents_organizer() Function

The `admission_documents_organizer()` function organizes image files of admission documents into folders.

## Inputs

The function takes no inputs.

## Outputs

The function outputs the image files organized into folders named after the type of document and university name identified from the image.

## Functionality

The function first loops through all the image files in the 'input' folder using `os.listdir('input')`. For each file, it checks if the filename ends with '.jpg' to filter for JPG image files.

For each JPG image file, it calls the `process_image()` function, passing the filename as a parameter. This function (not shown) presumably uses AI to analyze the image content and identify the type of document and university name.

The `process_image()` function returns this extracted information. If the AI could not identify the document type or university from the image, the function returns early without moving the file.

Otherwise, it constructs target folder and filename strings using the identified document type and university name. It checks if the 'output' folder exists, creating it if needed. The file is moved from the 'input' folder to the constructed path in 'output', renaming it in the process.

## Summary

In summary, `admission_documents_organizer()` automates organizing unlabeled admission document image files into folders based on their content using AI. The user simply drops files in 'input' and the code automatically files them into 'output' labeled by document type and university.
