📘 Interactive Kernel Filter Lab
A visual, interactive tool for learning image convolution  
（画像フィルタリングを学ぶためのインタラクティブ学習ツール）

🌟 Overview / 概要
Interactive Kernel Filter Lab is a small GUI application that lets users experiment with 3×3 convolution kernels and immediately see how they affect an image.
You can load any grayscale image, edit kernel values, choose presets, and inspect the exact 3×3 pixel neighborhood before and after filtering.

「Interactive Kernel Filter Lab」は、3×3 畳み込みカーネルを自由に編集し、画像にどのような効果が出るかをリアルタイムで確認できる学習用アプリです。
画像を読み込み、カーネル値を変更したり、プリセットを選んだり、フィルタ前後の 3×3 ピクセル値を比較できます。

✨ Key Features / 主な機能
🔹 Interactive Kernel Editing / カーネルのインタラクティブ編集
3×3 のカーネル値を直接入力

入力すると即座にフィルタ結果が更新

カーネルの合計値（Sum）を自動表示

🔹 Preset Filters / プリセットフィルタ
Identity（恒等）

Box Blur（ぼかし）

Sharpen（シャープ）

Edge Detection（エッジ検出）

Emboss（エンボス）

🔹 Pixel‑Level Inspection / ピクセル単位の観察
画像上をクリックして注目ピクセルを選択

矢印キーで 1 ピクセルずつ移動

選択位置の 元画像 3×3 と フィルタ後 3×3 を表示

🔹 Real‑Time Filtered Image / フィルタ後の画像表示
フィルタ結果を即時描画

選択ピクセル位置に赤いマーカーを表示

🖼️ How to Use / 使い方
1. Load an Image / 画像を読み込む
Click 「画像を読み込む」 and choose any image file.
The app converts it to grayscale and resizes it for display.

「画像を読み込む」を押して画像を選択します。
アプリは自動でグレースケール化し、表示用に縮小します。

2. Edit the Kernel / カーネルを編集
Enter numbers into the 3×3 grid.
The filtered image updates instantly.

3×3 の入力欄に数値を入れると、フィルタ結果がすぐに更新されます。

3. Choose a Preset / プリセットを選択
Use the dropdown menu to apply a preset kernel.

プルダウンメニューからプリセットを選ぶと、カーネルが自動入力されます。

4. Inspect Pixels / ピクセルを観察
Click the image to select a pixel

Use arrow keys to move

The 3×3 neighborhood (before/after filtering) appears on the right

画像をクリックしてピクセルを選択し、矢印キーで移動できます。
右側に元画像とフィルタ後の 3×3 ピクセル値が表示されます。

🧠 Educational Purpose / 教育的な意義
This tool is ideal for:

Learning how convolution works

Understanding blur, sharpen, edge detection

Teaching children or beginners with visual feedback

Experimenting with custom filters safely

このツールは以下に最適です：

畳み込みの仕組みを学ぶ

ぼかし・シャープ・エッジ検出の理解

子どもや初心者への視覚的な説明

カスタムフィルタの安全な実験

🛠️ Requirements / 必要環境
Python 3.x

Tkinter（標準で付属）

NumPy

Pillow

SciPy（convolve2d を使用）
