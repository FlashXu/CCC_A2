<template>
  <div>
    <div class="page-header page-header-small">
      <parallax
        class="page-header-image"
        style="background-image: url('img/moon.jpg')"
      >
      </parallax>
      <div class="content-center">
        <div class="container">
          <h1 class="title">This is our great team.</h1>
          <div class="text-center">
          </div>
        </div>
      </div>
    </div>

    <div class="section section-about-us">
      <div class="container">
        <div class="row">
          <div class="col-md-8 ml-auto mr-auto text-center">
            <h2 class="title">Who we are?</h2>
            <h5 class="description">
              Master students at the University of Melbourne with the degree varies from Information Technology 
              to Data Science. 
            </h5>
          </div>
        </div> 
      </div>
    </div>
    <div class="section section-team text-center">
      <div class="container">
        <h2 class="title">Here is our team</h2>
        <div class="team">
          <div class="row">

            <div class="col-md-4">
              <div class="team-player">
                <img
                  src="img/a1.png"
                  alt="Thumbnail Image"
                  class="rounded-circle img-fluid img-raised"
                  height="150"
                  width="150"
                />
                <h4 class="title">Qiangxing Lin</h4>
                <p class="category text-primary">Backend Engineer</p>
              </div>
            </div>

            <div class="col-md-4">
              <div class="team-player">
                <img
                  src="img/a2.png"
                  alt="Thumbnail Image"
                  class="rounded-circle img-fluid img-raised"
                  height="150"
                  width="150"
                />
                <h4 class="title">Yichao Xu</h4>
                <p class="category text-primary">Vue Developer</p>
              </div>
            </div>

            <div class="col-md-4">
              <div class="team-player">
                <img
                  src="img/a3.png"
                  alt="Thumbnail Image"
                  class="rounded-circle img-fluid img-raised"
                  height="150"
                  width="150"
                />
                <h4 class="title">Wentao Hao</h4>
                <p class="category text-primary">Vue Developer</p>
              </div>
            </div>

            <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>

            <div class="col-md-4">
              <div class="team-player">
                <img
                  src="img/a5.png"
                  alt="Thumbnail Image"
                  class="rounded-circle img-fluid img-raised"
                  height="150"
                  width="150"
                />
                <h4 class="title">Catrina</h4>
                <p class="category text-primary">Data Analyst</p>
              </div>
            </div>

            <div class="col-md-4">
              <div class="team-player">
                <img
                  src="img/a4.png"
                  alt="Thumbnail Image"
                  class="rounded-circle img-fluid img-raised"
                  height="150"
                  width="150"
                />
                <h4 class="title">Kaixin Chen</h4>
                <p class="category text-primary">Vue Developer</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { Button } from '@/components';
export default {
  name: 'team',
  bodyClass: 'team-page',
  components: {
    [Button.name]: Button
  }
};
</script>


<style></style>
