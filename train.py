# © 2021 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

from gan.optimizer import *
from data.generator import *
from data.sampling import *

from tqdm import tqdm
from tensorflow import GradientTape
from tensorflow import train as t

def train_step(gen, dsc, gen_opt, disc_opt, font_images, noise):
    with GradientTape() as gen_tape, GradientTape() as dsc_tape:
        generated_image = gen(noise, training=True)

        real = dsc(font_images, training=True)
        fake = dsc(generated_image, training=True)

        gen_loss = generator_loss(fake)
        dsc_loss = discriminator_loss(real, fake)

    gen_gradient = gen_tape.gradient(gen_loss, gen.trainable_variables)
    disc_gradient = dsc_tape.gradient(dsc_loss, dsc.trainable_variables)

    gen_opt.apply_gradients(zip(gen_gradient, gen.trainable_variables))
    disc_opt.apply_gradients(zip(disc_gradient, dsc.trainable_variables))

def train(gen, dsc, samples, bs, epochs, noise):
    gen_opt, disc_opt = generate_optimizer(1e-4)

    checkpoint_dir = 'checkpoints/'
    checkpoint_prefix = os.path.join(checkpoint_dir, 'ckpt')
    checkpoint = t.Checkpoint(
        generator_optimizer=gen_opt,
        discriminator_optimizer=disc_opt,
        generator=gen,
        discriminator=dsc
    )

    for epoch in range(epochs):
        dataset = DataGenerator(samples)
        dataset = dataset.generate(bs)
        for batch in tqdm(dataset, desc=f'{epoch+1} epochs'):
            train_step(gen, dsc, gen_opt, disc_opt, batch, noise)

        if not (epoch + 1) % 5:
            checkpoint.save(file_prefix=checkpoint_prefix)