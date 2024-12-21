from transformers import BartTokenizer, BartForConditionalGeneration

# Initialize the tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

def chunk_text(text, chunk_size=900):
    """Chunks the input text into smaller pieces to avoid truncation by the model."""
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def summarize_text_from_file(input_file, summary_ratio=0.5, max_summary_length=500, min_summary_length=100):
    """
    Summarize text from a file with dynamic summary length and chunking.

    Parameters:
    - input_file: Path to the input text file.
    - summary_ratio: Fraction of the input text length to use for the summary length.
    - max_summary_length: Maximum cap for the summary length.
    - min_summary_length: Minimum cap for the summary length.
    """
    try:
        with open(input_file, "r") as file:
            text = file.read()
        print("Text to summarize:\n", text)
    except FileNotFoundError:
        print(f"File {input_file} not found!")
        return None

    # Calculate dynamic lengths based on input text
    input_length = len(tokenizer.tokenize(text))  # Number of tokens in the input text
    dynamic_max_length = min(int(input_length * summary_ratio), max_summary_length)
    dynamic_min_length = max(min_summary_length, int(dynamic_max_length * 0.5))  # Ensure reasonable min length

    # Split text into chunks if it's too long
    chunks = chunk_text(text)

    summaries = []
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors='pt', truncation=True, padding=True, max_length=1024)
        summary_ids = model.generate(
            inputs['input_ids'],
            max_length=dynamic_max_length,
            min_length=dynamic_min_length,  # Allow model to generate more detailed summaries
            length_penalty=1.5,
            num_beams=8,  # Increased beam search for better quality summary
            early_stopping=True
        )
        summaries.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))

    # Combine all chunk summaries
    final_summary = ' '.join(summaries)
    return final_summary

if  _name_ == "_main_":
    input_file = "transcription.txt"  # Path to your input text file
    summary = summarize_text_from_file(input_file)
    if summary:
        print("\nSummary:\n",summary)