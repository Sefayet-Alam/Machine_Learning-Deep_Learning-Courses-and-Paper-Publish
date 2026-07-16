Resources:
1. Roboflow site: computer vision visualization, dataset upload clean, process and download
https://roboflow.com/ 

2. Supervision: library: visualize images for image process: https://github.com/roboflow/supervision 

3. ultra lyrics : roboflow's mother company 

4. object detection model: yolo,rf detr(real time data specialist),dino vision
5. human gesture detection: media-pipe
6. line draw in image (in video, to check if any moving object has crossed the line )

7. attention mechanism related: 
-> dense embedding vs sparse embedding
-> K,V,Q importance
-> why positional embedding is added? -> attention mechanism is parallel, RNN/LiSTM were sequential, so attention mechanism needs the positional values
-> each of 12 layers have multi-head attention (each head defines smth like parts of speech, positional value etc).
->Why do we add the input embeddings again? (why add and norm in the attention mechanism fig?)-> deep learning model's have linear transformations, so without the input , the model won't get the variance..
->FFN/MLP 
-> Why multi layer? -> early layers extract simple features, where later layers extract hidden/complex features
-> cross attention: encoder -> gives K vector , 
-> what is multihead cross attention? 
-> BERT models are basically stacked encoders
-> LLMs are basically stacked decoders
-> Encoder fixes the embeddings of each token, Decoder uses cross attention mechanism to align the input with those weights..Transformer = encoder + decoder 
-> 12 layers are sequential 