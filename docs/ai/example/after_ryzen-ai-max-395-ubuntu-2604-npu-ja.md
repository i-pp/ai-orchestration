---
title: "Ubuntu 26.04でRyzen AI MAX+ 395のNPUを動かすまで――IRONとC++推論の切り分け"
emoji: "🔬"
type: "tech"
topics: ["ryzenai", "ubuntu", "npu", "onnxruntime", "linux"]
published: false
---

## 忙しい人向け：目的・目標・結果と解決方法

### 目的と目標

GMKtec EVO-X3に搭載されたRyzen AI MAX+ 395のNPUを、Ubuntu 26.04から利用したい。

最終目標は、デバイスを認識させるだけでなく、C++からONNX RuntimeとVitis AI Execution Providerを使い、ONNXモデルの推論を完了することだ。

### 結果

**NPUでの推論に成功した。**

ただし、そこまでにいくつか問題があった。

- Ubuntuの`amdxdna`とシステムXRT 2.21.75で、NPUの診断やIRONのプログラムは動作した。
- Ryzen AI SDK 1.8.0のPythonバインディングは、手元のPython 3.14環境でABI互換性の問題に遭遇した。
- C++に切り替えるとONNXモデルのコンパイルまで進んだが、推論時に`XRT is not installed`と表示された。
- SDK用XRT 2.25.37を別領域へ展開し、実行時のライブラリ探索先を切り替えることで推論が完了した。

システムのXRTは入れ替えていない。

### 同じエラーで困っている人へ

今回の問題では、XRTの再インストールより先に、**失敗しているプロセスが実際にどのXRTを使っているか**を確認することが重要だった。

まず、NPUとドライバを確認する。

```bash
uname -r
lspci -nnk -d 1022:17f0
modinfo amdxdna
ls -l /dev/accel/ /dev/dri/renderD* 2>/dev/null
```

続いて、実行ユーザーのグループとmemlock制限を調べる。

```bash
id
ulimit -Sl
ulimit -Hl
prlimit --pid "$$" --memlock
```

NPUが見えていても、権限やmemlockの問題でXRTの検証が失敗することがある。

次に、XRTのインストール状況とライブラリを確認する。

```bash
dpkg-query -W '*xrt*'
ldconfig -p | grep -E 'libxrt_(core|coreutil)'
```

ここでXRTが存在していても、SDKが正しいライブラリを利用できているとは限らない。

実際に失敗するアプリケーションを`strace`で起動し、共有ライブラリの探索先を調べる。

```bash
strace -f -e trace=openat,openat2 \
  -o /tmp/npu-loader.strace \
  -- /path/to/your/quicktest

grep 'libxrt' /tmp/npu-loader.strace
```

`/path/to/your/quicktest`は、実際に失敗しているC++アプリケーションのパスへ置き換える。

私の失敗ログでは、次のシステムライブラリが開かれていた。

```text
/usr/lib/x86_64-linux-gnu/libxrt_coreutil.so.2
```

その後、SDK用XRT 2.25.37のbase、npu、XDNA pluginをローカルへ展開し、実行時に次の設定を使う構成へ変更した。

```bash
export XILINX_XRT="/path/to/local/opt/xilinx/xrt"
export LD_LIBRARY_PATH="$XILINX_XRT/lib:/path/to/sdk/onnxruntime/lib:/path/to/sdk/peano"
```

これは設定の要点を示したものだ。実際の配置先へ置き換える必要があり、SDKやC++アプリケーションの準備まで行うコマンドではない。

この構成で、次の結果を得た。

```text
Vitis AI EP registration: PASS
ONNX session creation: PASS
Running inference...
Inference: PASS
Quicktest: PASS
```

**すでにXRTとSDKを導入しているのに推論だけ失敗する場合は、まずライブラリの選択を確認してみてほしい。**

ゼロからの環境構築については、SDK配布物の取得、依存ライブラリの配置、C++アプリケーションのビルドまで含めたクリーンインストール検証がまだ完了していない。現時点では、上記を完全な新規導入手順としては扱わない。

ここまでが結論だ。

なぜIRONでは動くのにONNX Runtimeでは動かなかったのか。PythonのABI問題や共有ライブラリの探索をどう調べたのか。

その経緯が気になる人は、この先もどうぞ。

## NPUは動いている。それなのに「XRTがない」と言われる

GMKtec EVO-X3を手に入れたので、搭載されているRyzen AI MAX+ 395のNPUをUbuntuから使ってみることにした。

目標は単純だ。NPUがOSから認識されるだけではなく、実際にONNXモデルをコンパイルし、推論まで実行したい。

ところが、途中で妙な状況になった。

MLIR-AIEとIRONではNPUを使ったプログラムが動く。XRTの診断も通る。ONNX RuntimeでもVitis AI Execution Providerの登録とモデルのコンパイルまでは成功する。

それなのに、いざ推論を実行すると、こんなメッセージが出る。

```text
XRT is not installed. This InferenceSession generates model binaries only.
The session handle can not be used for inference run.
```

いや、XRTは入っている。さっきまでNPUを動かしていたじゃないか。

この食い違いを追いかけていくうちに、ドライバ、XRT、MLIR-AIE、Ryzen AI SDK、PythonのABI、共有ライブラリの探索順と、いくつもの境界を調べることになった。

最終的には、**システムのXRTを残したまま、Ryzen AI SDK用のXRTを別に配置する**ことで、C++からONNX Runtimeを使った推論を完了できた。

この記事では、そこに至るまでの経緯を振り返る。

なお、実際に成功した環境の記録と、新しいUbuntuへ導入するための未検証手順は区別している。独立したクリーンインストールでの再現と、CPUとの推論出力の数値比較は今後の課題だ。

## 今回の環境

使ったマシンはGMKtec EVO-X3。Ryzen AI MAX+ 395を搭載したミニPCだ。

調査を終えた時点の構成は次のとおり。

| 項目 | 構成 |
|---|---|
| PC | GMKtec EVO-X3 |
| CPU / NPU | AMD Ryzen AI MAX+ 395 |
| OS | Ubuntu 26.04.1 LTS |
| Kernel | 7.0.0-42-generic |
| NPUドライバ | amdxdna |
| ファームウェア | 1.1.2.65に対応するファイルを確認 |
| システムXRT | 2.21.75 |
| SDK用XRT | 2.25.37 |
| MLIR-AIE | `e28f6dc7e52fbb7b43f94b3693083c3f01a2387c` |
| Ryzen AI SDK | 1.8.0 |
| ONNX Runtime | 1.27.0 |
| 成功した実行経路 | C++ → ONNX Runtime C API → Vitis AI EP → NPU |

この組み合わせ全体がAMDの公式サポート構成という意味ではない。

特にPython環境は少し厄介だった。AMDのSDKインストーラーはPython 3.12を前提としているのに、調査対象として残っていた仮想環境はPython 3.14.4だった。

また、初期の記録にはカーネル7.0.0-38、その後には7.0.0-42が登場する。更新の全手順は回収できていないため、カーネル更新が推論成功の必須条件だったとは判断していない。

## まずはNPUがどこまで使えるのか

### ドライバを入れる前に、現状を調べる

Linuxでハードウェアが動かないと、ついドライバのインストールから始めたくなる。

しかし、今回のUbuntuでは、最初から`amdxdna`が存在していた。NPUのデバイスノードも作られ、実行ユーザーはrenderグループに所属していた。

この段階でドライバを入れ直しても、問題を増やすだけかもしれない。

そこで、まずPCIデバイス、カーネルドライバ、起動ログを確認した。

```bash
uname -r
lspci -nnk -d 1022:17f0
modinfo amdxdna
journalctl -k --no-pager -g 'amdxdna|amdnpu' -n 100
```

保存された起動ログには、amdxdnaドライバ0.7.0と、次のファームウェアをロードする記録があった。

```text
amdnpu/17f0_11/npu_7.sbin
```

ディスク上の対応するリンクは1.1.2.65を指していた。

ここで確認できたのは、カーネル側のNPU初期化が進んでいることだ。ユーザー空間のXRTや、さらに上位のSDKが動くかどうかは別問題になる。

### memlockが8 MiBでは足りなかった

XRTを導入して検証を進めると、今度はメモリ確保で引っかかった。

当初のシェルのmemlock上限は約8 MiB。64 MiBのマッピングを試したところ、`-11`で失敗した記録が残っている。

一方、rootでmemlockを無制限にした実行では、`xrt-smi examine`がデバイスを検出した。

これでmemlock制限が怪しくなった。ただし、同時に実行ユーザーも変わっているため、この比較だけで原因を完全に特定できたわけではない。

調べてみると、Linuxのリソース制限にはsoft limitとhard limitがあり、通常のユーザーが自分のhard limitを自由に引き上げられるわけではない。

実際、128 MiBへの引き上げを試したときには`EPERM`になった。

確認に使ったのは次のコマンドだ。

```bash
ulimit -Sl
ulimit -Hl
prlimit --pid "$$" --memlock
```

最終的には、PAM側に`1048576` KiB、systemd側に`LimitMEMLOCK=1G`という設定が残った。

systemdのdrop-inは次の場所に配置されている。

```text
/etc/systemd/system/user@.service.d/99-memlock.conf
```

途中ではdrop-inの配置先を間違えており、後から修正している。

ここで注意したいのは、**設定ファイルを変更したことと、実行中のプロセスへ反映されたことは別**だという点だ。

シェル、ユーザーマネージャー、そこから起動した子プロセスで制限が異なる可能性がある。最終的には対象プロセスの`/proc/<pid>/limits`まで確認する必要があった。

また、NPUのデバイス権限も、アカウントDB上のrenderグループ所属だけでは判断できない。実際のログインセッションからデバイスノードへアクセスできるかを確認する。

このあたりはNPU固有の話ではないが、Linuxでアクセラレータを使う際には意外と重要になる。

### XRTの検証は通った

memlockの問題を越えると、XRTの診断を実行できるようになった。

途中でテスト用の`xrt_smi_strx.a`が不足する問題もあった。rootと一般ユーザーではホームディレクトリもキャッシュも異なるため、同じXRTを使っていても必要なファイルが揃っているとは限らない。

最終的に、当時の端末出力ではrootのPerformanceモード、一般ユーザーのDefaultモードの両方で検証がPASSしている。

GEMMの診断結果は51.0 TOPSだった。

ただし、これはXRTの診断が報告した値であって、ONNXモデルの推論性能ではない。元の完全な測定条件も回収できていないため、ここで一般的な性能比較をするつもりはない。

それでも、NPUを利用するための下位層がある程度動いていることは分かった。

次は、実際にNPUへプログラムを送り込んでみる。

## MLIR-AIEとIRONを動かす

### ONNX Runtimeとは別の経路を確かめる

今回、MLIR-AIEとIRONを試したことには大きな意味があった。

Ryzen AI SDKへONNXモデルを渡す前に、NPU向けのプログラムを別の開発環境から実行できるか確かめられるからだ。

利用したのは[Xilinx/mlir-aie](https://github.com/Xilinx/mlir-aie)で、保存されているcheckoutは次のコミットだった。

```text
e28f6dc7e52fbb7b43f94b3693083c3f01a2387c
```

インストール済み環境から確認できたバージョンは以下のとおり。

| コンポーネント | バージョン |
|---|---|
| Python | 3.14.4 |
| mlir-aie | 1.4.5.dev113+ge28f6dc |
| llvm-aie | 22.0.0.2026102001+4f5df13d |
| NumPy | 2.5.4 |

ここでもPythonのバージョンが問題になった。

`utils/env_install.sh`はPython 3.12を既定としているだけでなく、minor versionを明示的に検査していた。

`PYTHON`変数を3.14へ変更するだけでは通らず、保存されたソースにはバージョンチェックを3.14へ変更した差分が残っている。

もっとも、チェックを通過させたからといって、Pythonのネイティブ拡張まで互換になるわけではない。

実際、環境を後から調べると、`mlir-aie`のwheelは`cp314-cp314`なのに、同じ仮想環境の`llvm-aie`には`cp310-cp310`というタグが残っていた。

通常のpipによる再インストールで同じ環境を構築できるとは限らない。

当時の環境で実行できたことと、その環境を新規に再構築できることは、ここでも分けて考える必要がある。

### IRONで最初に遭遇したのはPythonの探索パス

IRONのサンプルを動かす際にも、最初からすんなり成功したわけではなかった。

初期の実行では、次のようなエラーが出ていた。

```text
CPUOnlyTensor
Unsupported device: npu
```

NPU自体がサポートされていないのかと思いたくなるが、調べるとシステムPythonからは`pyxrt`をimportできる一方、仮想環境からは見えていなかった。

つまり、まず疑うべきはデバイスではなくPythonのモジュール探索範囲だった。

保存された仮想環境には、システム側のcp314用`pyxrt`へ向けたシンボリックリンクが残っている。

正確な作成コマンドは回収できていないが、当時のエラーと現在の環境の対応は確認できる。

その後の端末記録には、SAXPYと`vector_reduce_max`のPASSが残っていた。

### memcpyの実行結果とDMA警告

さらに`programming_examples/getting_started/00_memcpy/`も試している。

当時の会話に残された端末出力には、次の結果がある。

```text
Effective bandwidth (NPU avg): 80.19 GB/s
PASS!
```

平均end-to-end時間は約1849 µsだった。

ただし、この値は元の実行環境で再測定したものではない。公開用の証拠整理では、元の端末ログ全体と実行条件を再照合する必要がある。

ソースコードから分かるのは、int32を16777216要素送り、同じ大きさの出力を受け取ること。転送量の計算対象は合計128 MiBになる。

また、コンパイル時にはDMAバッファディスクリプタの再利用に関する警告も出ていた。

ディスクリプタを解放した後、DMAの完了保証がない状態で再利用している可能性を指摘する内容だ。

結果がPASSしたからといって、この警告を無害と決めつけることはできない。同期やディスクリプタの寿命については、繰り返し実行も含めて確認したい。

それでも、IRONからNPUへプログラムを送り、実行できたことは重要だった。

少なくとも「NPUハードウェアがまったく動いていない」という説明は成り立ちにくくなる。

そして、ここからが本題だ。

**IRONでは動く。しかし、Ryzen AI SDKではまだ動かない。**

## Ryzen AI SDKでPythonの壁にぶつかる

### インストーラーが要求するPython 3.12

ONNXモデルの推論にはRyzen AI SDK 1.8.0を使った。

配布物には、ONNX Runtime、VOE、コンパイラー関連ライブラリ、各種wheel、C++向けのファイルなどが含まれている。

まず`install_ryzen_ai.sh`を調べたところ、Python 3.12を明示的に呼び出していた。

インストーラーは仮想環境の作成、依存パッケージの導入、activateスクリプトへの設定追加、アーカイブの展開などを行う。

既存のインストール先ディレクトリを拒否する処理もあるので、動いている環境へ気軽に再実行できるものではない。

AMDの[公式Linux向けドキュメント](https://ryzenai.docs.amd.com/en/main/linux.html)も確認したが、Ubuntu 26.04の手元環境とは前提が異なる部分がある。

当時のAPTではPython 3.12の候補を見つけられなかった。

そこで、インストーラーにあるPython 3.12の参照を3.14へ変更する試行を行っている。

結果から言うと、これはうまくいかなかった。

### Pythonのバージョンチェックを越えてもABIで止まる

ONNX RuntimeをPythonからimportしようとすると、最初は実行可能スタックに関するエラーが出た。

ELFのスタック属性を変更した後は、さらに別のエラーになった。

```text
undefined symbol: _PyThreadState_UncheckedGet
```

Python 3.14側で必要なシンボルを解決できていない。

ここで重要なのは、問題が一つではなかったことだ。

最初の実行可能スタックの問題を越えても、CPythonのABIに関する問題が残っていた。

しかも、wheelのファイル名だけでは判断できない。

ONNX Runtimeのwheelは`py3-none-linux_x86_64`を名乗っていたが、内部にはネイティブの共有ライブラリが含まれている。VOEにも`cpython-312`を名前に持つ拡張があった。

パッケージをインストールできたことと、実際にimportして動かせることは違う。

Python 3.12を別途用意して検証する選択肢もあったが、今回は別の方向へ進むことにした。

**Pythonバインディングを通さず、C++からONNX RuntimeのC APIを直接呼ぶ。**

Python 3.14への対応が成功したわけではない。問題が起きているAPI境界を避ける方法だ。

## C++でも依存ライブラリは一筋縄ではいかない

### ONNX RuntimeのC APIを使う

C++側ではONNX Runtime 1.27.0のC APIを利用した。

ここでいうC APIは、C++ラッパーAPIとは別のものだ。

対応するバージョンのヘッダーを揃え、`onnxruntime_c_api.h`だけでなく、そこから参照される`onnxruntime_ep_c_api.h`も用意した。

ヘッダーの準備ができると、今度はVitis AI EPの登録処理でloggerの初期化順序に引っかかった。

`OrtEnv`を作成してからEPをセッションオプションへ登録するように整理し、先へ進めた。

ところが、モデルのコンパイルを進めると、今度はPeanoの共有ライブラリが見つからない。

```text
libpeano-lib.so.21.0git
```

調べると、必要なPeanoはSDK側の`llvm_aie` wheelに含まれていた。

IRONで使っているLLVM-AIE 22と、SDK側のPeano 21.0gitは同一ではない。

ここを混ぜてしまうと、別の不整合を持ち込むことになる。

`readelf`でSDKの`libxcompiler-mlir-e2e.so`を調べると、この21.0gitのライブラリを直接要求していた。

アプリケーションのリンクが成功したからといって、後からロードされるEPやコンパイラーの依存がすべて解決したとは限らない。

ようやく、モデルのコンパイルまで進めるようになった。

### モデルのコンパイルには成功した

使ったのはSDKのquicktestに含まれる`test_model.onnx`だ。

モデルの入出力は次の構成になっている。

```text
Input : float32 [1, 3, 32, 32]
Output: float32 [1, 10]
```

入力にはseed 42の乱数を使った。

Vitis AI EPの登録が成功し、モデルのコンパイルも完了した。

ところが、実際に`Run`を呼ぶと失敗する。

ログにはこう出ていた。

```text
ONNX Runtime: 1.27.0
Vitis AI EP registration: PASS

INFO: [VAIP-VAIML-CUSTOMOP] XRT is not installed.
This InferenceSession generates model binaries only.
The session handle can not be used for inference run.

Skipping execution in compile-only mode
```

さらに、出力テンソルに関するエラーが発生した。

```text
the ort_value must contain a constructed tensor or sparse tensor
```

ここで一度、状況を整理する必要があった。

- NPUはOSから認識されている。
- XRTの検証は通っている。
- IRONではNPUプログラムが実行できている。
- Vitis AI EPの登録は成功する。
- ONNXモデルのコンパイルも成功する。
- しかし、ONNX Runtimeの推論実行は失敗する。

つまり、問題は単純な「NPUが使えない」ではない。

モデルのコンパイルと、コンパイル済みモデルの実行の間に境界がある。

そして、ランタイムはその境界を越えられていなかった。

## XRTは入っている。では、どのXRTを使っている？

### straceで実際のライブラリ探索を見る

「XRTがない」というメッセージを見て、XRTを再インストールするのは簡単だ。

しかし、すでに別の経路では動いている。

そこで、失敗するプロセスがどのファイルを開いているのか調べた。

使用したのは`strace`だ。

```bash
strace -f \
  -e trace=openat,openat2,access,ioctl \
  -o /tmp/ryzenai-quicktest.strace \
  ./cpp-test/quicktest \
  > /tmp/ryzenai-quicktest.log 2>&1
```

保存された失敗ログには、次の行があった。

```text
openat(
  AT_FDCWD,
  "/usr/lib/x86_64-linux-gnu/libxrt_coreutil.so.2",
  O_RDONLY|O_CLOEXEC
) = 3
```

XRTの共有ライブラリは存在していたし、ファイルを開くことにも成功していた。

ただし、これだけではXRTの初期化が成功したとは言えない。

ファイルを開けたことと、SDKがそのランタイムを利用できたことは別だ。

それでも、少なくとも「XRTが物理的に存在しない」という説明では足りないことが分かった。

### システムXRTとSDK用XRTの違い

当時のシステムXRTは2.21.75だった。

一方、Ryzen AI SDKの配布物には2.25.37のXRTが含まれていた。

両方の`libxrt_coreutil.so.2`は同じSONAMEを持っている。

`readelf`などで依存関係や参照シンボルを調べたところ、確認した範囲ではEPが直接参照するXRT系53名、Dynamic Dispatchの61名は両方に存在していた。

つまり、単純に「古いXRTには必要なシンボルがない」とは言えなかった。

共有ライブラリの互換性は、シンボル名が揃っていれば保証されるものではない。ABI、オブジェクトレイアウト、プラグイン初期化、動的ロードなど、ほかにも確認すべきことがある。

また、`RUNPATH`は依存ライブラリの探索に関係するが、子の依存へ無条件に引き継がれるものではない。

アプリケーションを`ldd`で確認しただけでは、後からロードされるライブラリの選択まで把握できない。

そこで、システムXRTを入れ替えるのではなく、SDK用のXRTをローカルへ配置して、実行プロセスごとに選択することにした。

## システムXRTを残して、SDK用のXRTを使う

AMDの`RAI_1.8_Linux_NPU_XRT.zip`には、XRTのbase、npu、XDNA pluginのDEBが含まれていた。

これらを`dpkg-deb -x`でローカルディレクトリへ展開する。

システムのdpkg管理下にあるXRTは変更しない。

最終的に成功した起動スクリプトがこれだ。

```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

XRT_ROOT="$ROOT/xrt-2.25.37/opt/xilinx/xrt"
SDK_LIB="$ROOT/cpp-test/sdk/onnxruntime/lib"
PEANO_LIB="$ROOT/cpp-test/peano"

cd "$ROOT"

exec env \
  XILINX_XRT="$XRT_ROOT" \
  LD_LIBRARY_PATH="$XRT_ROOT/lib:$SDK_LIB:$PEANO_LIB" \
  "$ROOT/cpp-test/quicktest" "$@"
```

このスクリプトの要点は二つある。

一つ目は、`XILINX_XRT`をSDK用のローカルXRTへ向けること。

二つ目は、`LD_LIBRARY_PATH`でライブラリの探索順を明示することだ。

```text
1. ローカルXRTのlib
2. SDKのONNX Runtimeライブラリ
3. SDKのPeanoライブラリ
```

元の環境に残っていた`LD_LIBRARY_PATH`を後ろへ追加せず、実行に必要な探索パスを限定している。

これならIRONではシステムXRT、SDKのC++アプリケーションではローカルXRTというように、プロセスごとに使い分けられる。

成功時のローダーログでは、ローカルの`libxrt_coreutil`、`libxrt_core`、`libxrt_driver_xdna.so.2`の初期化が確認できた。

ただし、今回変更したのはXRTのバージョンだけではない。プラグイン、環境変数、探索順も同時に変わっている。

したがって、これらのうちどれが唯一の原因だったのかまでは特定できていない。

それでも、**実際に成功した構成を、システムXRTを壊さず再現できる形で残せた**ことには意味がある。

## ようやくNPUで推論できた

この構成でquicktestを実行すると、ONNX RuntimeはNPUを検出し、Vitis AI EPによるモデルのコンパイルと実行まで進んだ。

保存された成功ログには、次の割当がある。

```text
    NPU   398
VITIS_EP_CPU     2
```

さらに、NPUサブグラフについて次の報告が出ている。

```text
NPU     1
Actually running on NPU      1
```

アプリケーション側の結果も成功だった。

```text
ONNX Runtime: 1.27.0
Vitis AI EP registration: PASS
ONNX session creation: PASS
Output count: 1
Running inference...
Inference: PASS
Output[0]: output
Quicktest: PASS
```

ようやく、最初の目標に到達した。

ここで重要なのは、モデルをコンパイルできただけではなく、`Run`が完了したことだ。

失敗していたときには、NPUへの演算子割当が報告されていても、実際の推論は完了していなかった。

今回はランタイムがNPUサブグラフの実行を報告し、アプリケーションも推論完了まで到達している。

ただし、398対2という演算子数は、NPU使用率や実行時間の比率を意味しない。

また、元のquicktestは出力の数と名前を表示するものの、数値をCPUの参照結果と比較してはいなかった。

つまり、今回確認できたのは**NPUを使った推論経路が完了したこと**であって、数値精度まで検証できたわけではない。

成功時にも`No driver detection supported`などの警告は残っていた。

これらは今回の推論完了を妨げなかったが、すべての関連機能で無害と確認したわけではない。

## 別のUbuntuで再現するなら

ここまでの失敗を、新しい環境でも順番に再現する必要はない。

特に、Python 3.14へSDKのバージョンチェックを変更したり、実行可能スタックの属性を変更したりする試行は、C++推論を動かすための必須手順ではない。

今回の結果から考えると、C++推論を目的とするなら次の順序が合理的だ。

| 順序 | 作業 | 確認すること |
|---|---|---|
| 1 | PCI、amdxdna、ファームウェアを確認 | NPUの初期化 |
| 2 | デバイス権限とmemlockを確認 | 実行ユーザーからのアクセス |
| 3 | SDK配布物を取得 | ライセンス、バージョン、ハッシュ |
| 4 | SDK用XRTを別領域へ展開 | base、npu、XDNA plugin |
| 5 | ONNX RuntimeのC APIアプリをビルド | ヘッダー、リンク、共有ライブラリ |
| 6 | Vitis AI EPで推論を実行 | `Run`完了とNPU実行報告 |
| 7 | CPUとNPUの出力を比較 | 数値の妥当性 |

ただし、この手順は独立したクリーンインストールで一通り実証したものではない。

元環境で使われた一部のSDKアーカイブは完全なハッシュを回収できておらず、別のUbuntuで必要になる共有ライブラリやパッケージの対応も確定していない。

そのため、現時点では「誰でもこの手順だけで同じ結果になる」とは書けない。

また、MLIR-AIEとIRONを使いたい場合には、C++推論とは別にPython環境とwheelの互換性を解決する必要がある。

今回の調査をもとに、環境の検査、配布物の展開計画、実行結果の保存、出力比較のための補助スクリプトも整理した。

それらは、過去の成功ログを読み込んだだけで新しい環境の検証成功と判定しない設計にしている。

実際に新規実行していない項目はSKIPとして扱う。

## 同じ問題に遭遇したら

今回の調査で役に立った確認箇所をまとめておく。

| 症状 | 最初に確認すること |
|---|---|
| NPUが見えない | PCIデバイス、amdxdna、起動ログ |
| デバイスノードへアクセスできない | renderグループ、ACL、実行セッション |
| メモリ確保に失敗する | soft/hard memlock、プロセスの制限 |
| XRTの検証ファイルが見つからない | XRTの版、ユーザーごとのキャッシュ |
| IRONで`Unsupported device: npu` | 仮想環境から`pyxrt`が見えるか |
| Pythonでネイティブ拡張をimportできない | Python ABI、wheelタグ、ELF属性 |
| EP登録時にloggerエラー | `OrtEnv`の初期化順序 |
| Peanoの共有ライブラリがない | SDKコンパイラーの`DT_NEEDED` |
| XRTがあるのにcompile-onlyになる | 実際にロードされたXRTとプラグイン |
| 演算子割当はあるが推論が失敗する | `Run`の結果、出力テンソルの状態 |

特に、ランタイムの問題を調べるときは、パッケージのインストール状況だけで判断しない方がいい。

実行中のプロセスがどの共有ライブラリを開き、どこまで初期化できているかを調べると、見えてくるものが変わる。

`strace`、`readelf`、`LD_DEBUG`は、そのための有力な道具になる。

## おわりに

最初は、UbuntuでNPUを認識させてONNXモデルを動かすだけのつもりだった。

実際には、ドライバ、メモリ制限、XRT、MLIR-AIE、IRON、Python、ONNX Runtime、Peanoと、いくつもの層を行き来することになった。

その中でも印象的だったのは、IRONではNPUが動いているのに、ONNX Runtimeからは「XRTがインストールされていない」と言われたことだ。

エラーメッセージは調査の入口にはなるが、それだけで原因を決めてはいけない。

今回の場合、XRTの存在を確認するだけでは不十分だった。実際にどのライブラリが選ばれ、どの実行経路が成功しているのかを分けて調べる必要があった。

結果として、システムXRTを維持しながら、SDK用XRTをプロセス単位で切り替える構成に落ち着いた。

まだ終わっていないこともある。

Python SDKを適切な3.12環境で動かすこと、MLIR-AIEのwheel構成を再現可能にすること、DMA警告の影響を確認すること、別のUbuntu環境でクリーンインストールを検証すること。そして、CPUとNPUの推論出力を数値で比較することだ。

ただ、少なくとも今回は、**Ryzen AI MAX+ 395のNPUで、C++からONNX Runtimeの推論を完了するところまで到達できた。**

次は「動いた」の先へ進みたい。

同じモデルと入力でCPUとNPUの出力を比較し、精度と性能を測れる状態まで持っていくつもりだ。

---

*この記事は実機の作業記録と保存されたログをもとに構成した。過去の実行結果、後から確認した環境状態、未検証の再現手順は区別している。詳細な調査記録、依存関係、証拠索引、検証スクリプトは別途Gitリポジトリに整理している。公開時にはリポジトリへのリンクを追加する。*
