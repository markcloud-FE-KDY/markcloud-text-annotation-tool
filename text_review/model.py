from simpletransformers.t5 import T5Model


def get_engtokor(pretrained_model_path, diff_result: list):
    print("> get_engtokor...")

    model = T5Model(
        "mt5",
        pretrained_model_path,
        use_cuda=False,
        args={"max_seq_length": 48, "num_beams": 1},
    )

    model_result = model.predict(diff_result)

    return diff_result, model_result


if __name__=="__main__":
    print(get_engtokor("./best_model", ["tabox", "ta2box"]))
