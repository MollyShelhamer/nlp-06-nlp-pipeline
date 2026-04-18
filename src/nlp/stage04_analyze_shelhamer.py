"""
stage04_analyze_shelhamer.py
(EDIT YOUR COPY OF THIS FILE)

Source: analysis-ready Pandas DataFrame (from Transform stage)
Sink:   visualizations saved to data/processed/

======================================================================
THE ANALYST WORKFLOW: Analyze means look, not just calculate
======================================================================

Engineered features have no value until someone looks at them.

The Analyze stage makes the data visible:

  - frequency distributions show which words dominate the text
  - word clouds give an immediate gestalt of the content
  - bar charts allow comparison across documents or categories

In a single-document pipeline like this one, analysis is exploratory:
you are asking "what is in here?" before deciding what to do with it.

In a multi-document pipeline (Module 7 and beyond), analysis becomes
comparative: "how does this document differ from others?"

The same tools apply in both cases. The questions change.

======================================================================
PURPOSE AND ANALYTICAL QUESTIONS
======================================================================

Purpose

  Compute frequency distributions and produce visualizations
  that surface patterns in the cleaned text.

Analytical Questions

  - Which words appear most frequently in the cleaned abstract?
  - Does the frequency distribution look meaningful or noisy?
  - Does the word cloud reflect the actual topic of the paper?
  - What does the type-token ratio tell us about vocabulary richness?
  - Would a different cleaning strategy change the results?

======================================================================
NOTES
======================================================================

Following our process, do NOT edit this _case file directly.
Keep it as a working example.

In your custom project, copy this file and rename it
by appending _yourname.py.

Then edit your copy to:
  - adjust the number of top tokens shown
  - add additional visualizations
  - compare results across multiple documents
  - document what the visualizations reveal about your data
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

from collections import Counter
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# ============================================================
# Section 2. Define Helper Functions
# ============================================================


def _plot_top_tokens(
    tokens: list[str],
    top_n: int,
    output_path: Path,
    title: str,
    LOG: logging.Logger,
) -> None:
    """Plot a horizontal bar chart of the top N most frequent tokens.

    Args:
        tokens (list[str]): List of tokens from the cleaned abstract.
        top_n (int): Number of top tokens to display.
        output_path (Path): Path to save the chart image.
        title (str): Chart title.
        LOG (logging.Logger): The logger instance.
    """
    # Count token frequencies
    # Counter returns a dictionary-like object mapping each token to its count.
    # .most_common(top_n) returns the top_n most frequent tokens as a list of
    # (token, count) tuples: [("agents", 3), ("language", 2), ...]
    counter = Counter(tokens)
    most_common = counter.most_common(top_n)

    if not most_common:
        LOG.warning("No tokens to plot.")
        return

    # Unpack the list of tuples into two separate lists using zip()
    # words will be the list of tokens, counts will be the list of their frequencies.
    # strict=False allows zip to handle cases where there are fewer than top_n tokens without raising an error.
    words, counts = zip(*most_common, strict=False)

    # Create horizontal bar chart
    # Reversing the order puts the most frequent token at the top

    # Use plt.subplots to create a figure and axis object.
    # figsize sets the size of the figure in inches.
    fig, ax = plt.subplots(figsize=(10, 6))

    # barh creates a horizontal bar chart.
    # The y-values are the tokens (words),
    # and the x-values are their corresponding counts (frequencies).
    ax.barh(list(reversed(words)), list(reversed(counts)), color="steelblue")

    # Set labels and title
    ax.set_xlabel("Frequency")
    ax.set_title(title)

    # Adjust layout to prevent clipping of labels and title
    plt.tight_layout()

    # Save the figure to the specified output path with a resolution of 150 DPI.
    plt.savefig(output_path, dpi=150)

    # After saving, close the figure to free up memory and avoid displaying it in interactive environments.
    plt.close()

    LOG.info(f"  Saved bar chart to {output_path}")


def _plot_wordcloud(
    text: str,
    output_path: Path,
    title: str,
    LOG: logging.Logger,
) -> None:
    """Generate and save a word cloud from cleaned text.

    Word size reflects token frequency.
    More frequent words appear larger.

    Args:
        text (str): Space-joined cleaned token string.
        output_path (Path): Path to save the word cloud image.
        title (str): Title logged with the output.
        LOG (logging.Logger): The logger instance.
    """
    if not text or text == "unknown":
        LOG.warning("No text available for word cloud.")
        return

    # WordCloud generates the image from a string of space-separated words.
    # width/height set the image dimensions in pixels.
    # background_color sets the canvas color.
    # max_words limits the number of words shown.
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        max_words=80,
        colormap="viridis",  # or "plasma", "inferno", "magma", etc.
    ).generate(text)

    # Use plt.subplots to create a figure and axis object.
    # figsize sets the size of the figure in inches.
    fig, ax = plt.subplots(figsize=(12, 6))

    # imshow displays the generated word cloud image on the axis.
    ax.imshow(wc, interpolation="bilinear")

    # axis("off") hides the axes for a cleaner look.
    ax.axis("off")

    # Set the title of the plot using the provided title argument.
    ax.set_title(title, fontsize=14)

    # Adjust layout to prevent clipping of labels and title
    plt.tight_layout()

    # Save the figure to the specified output path with a resolution of 150 DPI.
    plt.savefig(output_path, dpi=150)

    # After saving, close the figure to free up memory and avoid displaying it in interactive environments.
    plt.close()

    LOG.info(f"  Saved word cloud to {output_path}")


def _plot_word_length_histogram(
    tokens: list[str],
    output_path: Path,
    title: str,
    LOG: logging.Logger,
) -> None:
    """Plot a histogram of word lengths from the tokens.

    Args:
        tokens (list[str]): List of tokens from the cleaned abstract.
        output_path (Path): Path to save the histogram image.
        title (str): Chart title.
        LOG (logging.Logger): The logger instance.
    """
    if not tokens:
        LOG.warning("No tokens to plot histogram.")
        return

    # Compute word lengths
    word_lengths = [len(token) for token in tokens]

    # Create histogram
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot histogram with bins for each possible length
    ax.hist(
        word_lengths,
        bins=range(1, max(word_lengths) + 2),
        edgecolor='black',
        alpha=0.7,
        color='skyblue',
    )

    # Set labels and title
    ax.set_xlabel("Word Length (characters)")
    ax.set_ylabel("Frequency")
    ax.set_title(title)

    # Adjust layout to prevent clipping of labels and title
    plt.tight_layout()

    # Save the figure to the specified output path with a resolution of 150 DPI.
    plt.savefig(output_path, dpi=150)

    # After saving, close the figure to free up memory and avoid displaying it in interactive environments.
    plt.close()

    LOG.info(f"  Saved word length histogram to {output_path}")


def _plot_comparative_metrics(
    df: pd.DataFrame,
    output_path: Path,
    LOG: logging.Logger,
) -> None:
    """Create a comparative bar chart of key metrics across papers.

    Args:
        df (pd.DataFrame): DataFrame with paper data.
        output_path (Path): Path to save the chart image.
        LOG (logging.Logger): The logger instance.
    """
    if df.empty:
        LOG.warning("No data to plot comparative metrics.")
        return

    # Prepare data for plotting
    paper_labels = [f"Paper {int(row['paper_index'])}" for _, row in df.iterrows()]
    token_counts = df['token_count'].tolist()
    type_token_ratios = df['type_token_ratio'].tolist()
    author_counts = df['author_count'].tolist()

    # Create subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Token count comparison
    axes[0].bar(paper_labels, token_counts, color='steelblue')
    axes[0].set_title('Token Count Comparison')
    axes[0].set_ylabel('Token Count')
    axes[0].tick_params(axis='x', rotation=45)

    # Type-token ratio comparison
    axes[1].bar(paper_labels, type_token_ratios, color='skyblue')
    axes[1].set_title('Type-Token Ratio Comparison')
    axes[1].set_ylabel('Type-Token Ratio')
    axes[1].tick_params(axis='x', rotation=45)

    # Author count comparison
    axes[2].bar(paper_labels, author_counts, color='lightcoral')
    axes[2].set_title('Author Count Comparison')
    axes[2].set_ylabel('Author Count')
    axes[2].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    LOG.info(f"  Saved comparative metrics chart to {output_path}")


def _plot_comparative_word_lengths(
    df: pd.DataFrame,
    output_dir: Path,
    LOG: logging.Logger,
) -> None:
    """Create comparative word length histograms for all papers.

    Args:
        df (pd.DataFrame): DataFrame with paper data.
        output_dir (Path): Directory to save the chart image.
        LOG (logging.Logger): The logger instance.
    """
    if df.empty:
        LOG.warning("No data to plot comparative word lengths.")
        return

    # Create a combined histogram
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
    max_length = 0

    for idx, row in df.iterrows():
        tokens_str = str(row.get("tokens", ""))
        tokens = tokens_str.split() if tokens_str else []
        if tokens:
            word_lengths = [len(token) for token in tokens]
            max_length = max(max_length, max(word_lengths))

            paper_index = int(row.get("paper_index", idx + 1))
            color = colors[(paper_index - 1) % len(colors)]

            ax.hist(
                word_lengths,
                bins=range(1, max_length + 2),
                alpha=0.5,
                label=f"Paper {paper_index}",
                color=color,
                edgecolor='black',
            )

    ax.set_xlabel("Word Length (characters)")
    ax.set_ylabel("Frequency")
    ax.set_title("Comparative Word Length Distributions")
    ax.legend()

    plt.tight_layout()
    output_path = output_dir / "comparative_word_lengths.png"
    plt.savefig(output_path, dpi=150)
    plt.close()

    LOG.info(f"  Saved comparative word lengths chart to {output_path}")


# ============================================================
# Section 3. Define Run Analyze Function
# ============================================================


def run_analyze(
    df: pd.DataFrame,
    LOG: logging.Logger,
    output_dir: Path = Path("data/processed"),
    top_n: int = 20,
) -> None:
    """Analyze the transformed DataFrame and produce visualizations.

    Args:
        df (pd.DataFrame): Analysis-ready DataFrame from Transform stage.
        LOG (logging.Logger): The logger instance.
        output_dir (Path): Directory to save visualization outputs.
        top_n (int): Number of top tokens to show in frequency chart.
    """
    LOG.info("========================")
    LOG.info("STAGE 04: ANALYZE starting...")
    LOG.info(f"Analyzing {len(df)} papers")
    LOG.info("========================")

    output_dir.mkdir(parents=True, exist_ok=True)

    # ============================================================
    # Phase 4.1: Extract token lists and summary stats from DataFrame
    # ============================================================
    # Process each paper in the DataFrame
    # ============================================================

    LOG.info("========================")
    LOG.info("PHASE 4.1: Extract tokens and summary statistics for all papers")
    LOG.info("========================")

    # Process each paper
    for idx, row in df.iterrows():
        paper_index = int(row.get("paper_index", idx + 1))
        arxiv_id = str(row.get("arxiv_id", "unknown"))
        title: str = str(row.get("title", "unknown"))
        tokens_str: str = str(row.get("tokens", ""))
        token_count: int = int(row.get("token_count", 0))
        unique_token_count: int = int(row.get("unique_token_count", 0))
        type_token_ratio: float = float(row.get("type_token_ratio", 0.0))
        abstract_word_count: int = int(row.get("abstract_word_count", 0))
        author_count: int = int(row.get("author_count", 0))

        # Split the space-joined token string back into a list
        tokens: list[str] = tokens_str.split() if tokens_str else []

        LOG.info(f"  Paper {paper_index} ({arxiv_id}): {title}")
        LOG.info(f"    Abstract word count (raw):    {abstract_word_count}")
        LOG.info(f"    Token count (clean):          {token_count}")
        LOG.info(f"    Unique token count:           {unique_token_count}")
        LOG.info(f"    Type-token ratio:             {type_token_ratio}")
        LOG.info(f"    Author count:                 {author_count}")

        # ============================================================
        # Phase 4.2: Frequency distribution - bar chart per paper
        # ============================================================

        LOG.info("========================")
        LOG.info(
            f"PHASE 4.2: Top {top_n} token frequency - bar chart (Paper {paper_index})"
        )
        LOG.info("========================")

        _plot_top_tokens(
            tokens=tokens,
            top_n=top_n,
            output_path=output_dir / f"case_top_tokens_paper_{paper_index}.png",
            title=f"Top {top_n} Tokens: {title[:50]}...",
            LOG=LOG,
        )

        # ============================================================
        # Phase 4.3: Word cloud per paper
        # ============================================================

        LOG.info("========================")
        LOG.info(f"PHASE 4.3: Word cloud (Paper {paper_index})")
        LOG.info("========================")

        _plot_wordcloud(
            text=tokens_str,
            output_path=output_dir / f"case_wordcloud_paper_{paper_index}.png",
            title=f"Word Cloud: {title[:50]}...",
            LOG=LOG,
        )

        # ============================================================
        # Phase 4.4: Word length distribution - histogram per paper
        # ============================================================

        LOG.info("========================")
        LOG.info(
            f"PHASE 4.4: Word length distribution - histogram (Paper {paper_index})"
        )
        LOG.info("========================")

        _plot_word_length_histogram(
            tokens=tokens,
            output_path=output_dir / f"case_word_lengths_paper_{paper_index}.png",
            title=f"Word Length Distribution: {title[:50]}...",
            LOG=LOG,
        )

    # ============================================================
    # Phase 4.5: Comparative analysis across papers
    # ============================================================

    LOG.info("========================")
    LOG.info("PHASE 4.5: Comparative analysis across papers")
    LOG.info("========================")

    # Create comparative visualizations
    _plot_comparative_metrics(df, output_dir / "comparative_metrics.png", LOG)
    _plot_comparative_word_lengths(df, output_dir, LOG)

    # ============================================================
    # Phase 4.6: Log comparative summary
    # ============================================================

    LOG.info("========================")
    LOG.info("PHASE 4.6: Comparative summary")
    LOG.info("========================")

    LOG.info("Comparative Statistics:")
    LOG.info(f"  Total papers: {len(df)}")
    LOG.info(f"  Average token count: {df['token_count'].mean():.1f}")
    LOG.info(f"  Average type-token ratio: {df['type_token_ratio'].mean():.4f}")
    LOG.info(f"  Average author count: {df['author_count'].mean():.1f}")

    LOG.info("Sink: visualizations saved to data/processed/")
    LOG.info("Analysis complete.")
